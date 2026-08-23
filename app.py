import streamlit as st
import time

from streamlit_autorefresh import st_autorefresh

from agents.content_agent import generate_challenge
# from agents.evaluation_agent import evaluate_recall, EVALUATION_STAGES
from config import (
    APP_NAME,
    WORD_LIMITS,
    DIFFICULTIES,
    READING_TIMES,
    WRITING_TIMES,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="centered",
)


# --------------------------------------------------
# PHASE CONFIGURATION
# --------------------------------------------------

PHASES = [
    ("setup", "Setup"),
    ("reading", "Reading"),
    ("recall", "Recall"),
    ("evaluation", "Evaluation"),
    ("result", "Result"),
]


# --------------------------------------------------
# EVALUATION TIMING
# --------------------------------------------------

SECONDS_PER_EVAL_STAGE = 0.7


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "stage" not in st.session_state:
    st.session_state.stage = "setup"


# --------------------------------------------------
# SIDEBAR PROGRESS
# --------------------------------------------------

current_stage_index = next(
    index
    for index, (stage, _) in enumerate(PHASES)
    if stage == st.session_state.stage
)


with st.sidebar:

    st.title("🧠 Cognify AI")

    st.subheader("Challenge Progress")

    for index, (_, label) in enumerate(PHASES):

        if index < current_stage_index:

            st.write(f"✓ {label}")

        elif index == current_stage_index:

            st.write(f"🔵 **{label}**")

        else:

            st.write(f"○ {label}")

    if "topic" in st.session_state and st.session_state.stage != "setup":

        st.divider()

        st.caption("Challenge Configuration")

        st.write(f"**Topic:** {st.session_state.topic}")

        st.write(f"**Difficulty:** {st.session_state.difficulty}")

        st.write(f"**Word Limit:** {st.session_state.word_limit}")

        st.write(f"**Reading Time:** {st.session_state.reading_time} min")

        st.write(f"**Writing Time:** {st.session_state.writing_time} min")


# --------------------------------------------------
# MAIN CONTENT AREA
# --------------------------------------------------
#
# Every phase is drawn inside this single placeholder so a stage
# switch always fully replaces whatever was here before.
#
# IMPORTANT: timers are driven by `st_autorefresh`, a client-side JS
# timer that triggers a normal, well-spaced script rerun every tick —
# NOT by calling `time.sleep()` followed by `st.rerun()` in a tight
# loop. That blocking loop is what was causing the passage to still
# be visible during Recall: firing `st.rerun()` recursively from
# inside a `sleep()` loop can outrun Streamlit's own delta ordering,
# so the frontend occasionally applies a stale "reading" delta after
# the "recall" one. Autorefresh reruns the whole script on a clean
# timer tick instead, so there's no loop for that race to happen in.

content_area = st.empty()

with content_area.container():

    # ==================================================
    # SETUP PHASE
    # ==================================================

    if st.session_state.stage == "setup":

        st.title("🧠 Cognify AI")

        st.write(
            "Test how well you can read, remember, and recall information."
        )

        st.subheader("Configure Your Challenge")

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Artificial Intelligence",
        )

        word_limit = st.selectbox(
            "Word Limit",
            WORD_LIMITS,
        )

        difficulty = st.selectbox(
            "Difficulty",
            DIFFICULTIES,
        )

        reading_time = st.selectbox(
            "Reading Time (minutes)",
            READING_TIMES,
        )

        writing_time = st.selectbox(
            "Writing Time (minutes)",
            WRITING_TIMES,
        )

        if st.button("Start Challenge"):

            if not topic.strip():

                st.warning("Please enter a topic.")

            else:

                with st.spinner("Generating your challenge..."):

                    challenge = generate_challenge(
                        topic=topic,
                        word_limit=word_limit,
                        difficulty=difficulty,
                    )

                st.session_state.challenge = challenge

                st.session_state.topic = topic
                st.session_state.word_limit = word_limit
                st.session_state.difficulty = difficulty
                st.session_state.reading_time = reading_time
                st.session_state.writing_time = writing_time

                # Reset phase-specific state
                st.session_state.pop("reading_start_time", None)
                st.session_state.pop("writing_start_time", None)
                st.session_state.pop("recall_text", None)
                st.session_state.pop("user_recall", None)
                st.session_state.pop("eval_start_time", None)
                st.session_state.pop("evaluation", None)

                # Set the reading deadline now, so the Reading phase
                # doesn't need its own "first run" initialization step.
                st.session_state.reading_start_time = time.time()

                # Move forward
                st.session_state.stage = "reading"

                content_area.empty()

                st.rerun()

        st.stop()

    # ==================================================
    # READING PHASE
    # ==================================================

    elif st.session_state.stage == "reading":

        # Ticks this script rerun once per second. No sleep, no
        # recursive rerun — just a normal, isolated rerun per tick.
        st_autorefresh(interval=1000, key="reading_timer_tick")

        st.title("📖 Reading Phase")

        challenge = st.session_state.challenge

        elapsed_time = time.time() - st.session_state.reading_start_time
        total_time = st.session_state.reading_time * 60
        remaining_time = max(0, total_time - elapsed_time)

        remaining_seconds = int(remaining_time)
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        # ----------------------------------------------
        # TIMER EXPIRED — checked BEFORE anything else is drawn,
        # so the passage is never written into this run at all.
        # ----------------------------------------------

        if remaining_time <= 0:

            st.session_state.pop("reading_start_time", None)
            st.session_state.stage = "recall"
            st.session_state.writing_start_time = time.time()

            content_area.empty()

            st.rerun()

        # ----------------------------------------------
        # READING CONTENT
        # ----------------------------------------------

        st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

        st.write(f"Topic: **{challenge.topic}**")
        st.write(f"Difficulty: **{challenge.difficulty}**")

        st.divider()

        # The passage is rendered ONLY here, and ONLY while
        # st.session_state.stage == "reading".
        st.write(challenge.content)

    # ==================================================
    # RECALL PHASE
    # ==================================================

    elif st.session_state.stage == "recall":

        st_autorefresh(interval=1000, key="recall_timer_tick")

        st.title("✍️ Recall Phase")

        st.write(
            "The passage has disappeared. "
            "Write everything you remember."
        )

        elapsed_time = time.time() - st.session_state.writing_start_time
        total_time = st.session_state.writing_time * 60
        remaining_time = max(0, total_time - elapsed_time)

        remaining_seconds = int(remaining_time)
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

        # ----------------------------------------------
        # RECALL INPUT
        # ----------------------------------------------
        # NOTE: `challenge.content` (the original passage) is never
        # read anywhere in this branch.

        recall = st.text_area(
            "Your Recall",
            placeholder="Write everything you remember...",
            height=300,
            key="recall_text",
        )

        # ----------------------------------------------
        # TIMER EXPIRED
        # ----------------------------------------------

        if remaining_time <= 0:

            st.session_state.user_recall = recall
            st.session_state.pop("writing_start_time", None)
            st.session_state.stage = "evaluation"
            st.session_state.eval_start_time = time.time()

            content_area.empty()

            st.rerun()

    # ==================================================
    # EVALUATION PHASE
    # ==================================================

    # elif st.session_state.stage == "evaluation":

    #     st_autorefresh(interval=400, key="evaluation_timer_tick")

    #     st.title("🔍 Evaluating Your Recall")

    #     st.write("Analyzing how accurately you remembered the passage...")

    #     elapsed_time = time.time() - st.session_state.eval_start_time
    #     current_stage_number = int(elapsed_time / SECONDS_PER_EVAL_STAGE)

    #     # ----------------------------------------------
    #     # STAGE CHECKLIST (visual feedback only — no internals of
    #     # the evaluation pipeline are exposed to the user)
    #     # ----------------------------------------------

    #     for index, label in enumerate(EVALUATION_STAGES):

    #         if index < current_stage_number:
    #             st.write(f"✓ {label}")
    #         elif index == current_stage_number:
    #             st.write(f"🔵 **{label}**")
    #         else:
    #             st.write(f"○ {label}")

    #     st.progress(min(current_stage_number / len(EVALUATION_STAGES), 1.0))

    #     # ----------------------------------------------
    #     # EVALUATION COMPLETE
    #     # ----------------------------------------------

    #     if current_stage_number >= len(EVALUATION_STAGES):

    #         challenge = st.session_state.challenge
    #         recall_text = st.session_state.get("user_recall", "")

    #         evaluation = evaluate_recall(
    #             passage=challenge.content,
    #             recall_text=recall_text,
    #         )

    #         st.session_state.evaluation = evaluation
    #         st.session_state.pop("eval_start_time", None)
    #         st.session_state.stage = "result"

    #         content_area.empty()

    #         st.rerun()

    # # ==================================================
    # # RESULT PHASE
    # # ==================================================

    # elif st.session_state.stage == "result":

    #     st.title("🏆 Your Recall Result")

    #     evaluation = st.session_state.evaluation

    #     st.header(f"{evaluation.score} / 100")
    #     st.progress(evaluation.score / 100)
    #     st.write(evaluation.summary)

    #     st.divider()

    #     st.subheader("What You Remembered Well")
    #     for point in evaluation.remembered_well:
    #         st.write(f"🟢 {point}")

    #     st.subheader("What You Missed")
    #     for point in evaluation.missed:
    #         st.write(f"🔴 {point}")

    #     st.subheader("AI Feedback")
    #     st.info(evaluation.ai_feedback)

    #     with st.expander("Evaluation Details"):
    #         for label, value in evaluation.metrics.items():
    #             st.write(f"**{label}:** {value}")

    #     st.divider()

    #     if st.button("Start a New Challenge"):

    #         for key in list(st.session_state.keys()):
    #             st.session_state.pop(key, None)

    #         st.session_state.stage = "setup"

    #         content_area.empty()

    #         st.rerun()