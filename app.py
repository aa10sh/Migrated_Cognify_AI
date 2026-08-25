import streamlit as st
import streamlit.components.v1 as components
import time

from agents.content_agent import generate_challenge
from graph.evaluation_graph import evaluation_graph

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

# Streamlit dims/fades elements briefly every time a fragment reruns,
# to indicate "updating" state. With run_every=1 on our timer
# fragments, this fires every second during Reading/Recall and reads
# as a distracting screen dim/blur flicker, even though it's purely
# cosmetic and doesn't affect widget state or typing. Neutralize it.
st.markdown(
    """
    <style>
    [data-stale="true"] {
        opacity: 1 !important;
        transition: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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
# SESSION STATE
# --------------------------------------------------

if "stage" not in st.session_state:
    st.session_state.stage = "setup"


# --------------------------------------------------
# PHASE TRANSITION HELPERS
# (shared by fragments and normal button clicks)
# --------------------------------------------------

def _finish_reading():
    """Called when the reading timer expires."""
    st.session_state.pop("reading_start_time", None)
    st.session_state.stage = "recall"
    st.session_state.writing_start_time = time.time()
    st.rerun(scope="app")


def _inject_recall_autosync():
    """
    st.text_area only commits its value to session_state on blur or
    Ctrl+Enter - not on every keystroke. That means if the recall timer
    expires (or Submit is clicked) while the user is still mid-keystroke
    and hasn't blurred, whatever they typed since their last commit may
    never have reached the server at all, and recall_text comes through
    empty/stale even though the user visibly typed something.

    This injects a tiny background script that, once a second, blurs
    and immediately refocuses the recall textarea (only if it's
    currently focused), preserving cursor position. That forces
    Streamlit's normal blur-commit behavior to fire continuously, so
    session_state["recall_text"] stays at most ~1s stale no matter
    when the timer expires or Submit is pressed - without interrupting
    the user's typing.
    """
    components.html(
        """
        <script>
        setInterval(() => {
            const doc = window.parent.document;
            const active = doc.activeElement;
            if (active && active.tagName === "TEXTAREA") {
                const start = active.selectionStart;
                const end = active.selectionEnd;
                active.blur();
                active.focus();
                active.setSelectionRange(start, end);
            }
        }, 1000);
        </script>
        """,
        height=0,
    )


def submit_recall():
    """Called when the recall timer expires OR the user clicks Submit."""
    recall_text = st.session_state.get("recall_text", "")
    st.session_state["user_recall"] = recall_text
    st.session_state.pop("writing_start_time", None)
    st.session_state.stage = "evaluation"
    st.rerun(scope="app")


# --------------------------------------------------
# TIMER FRAGMENTS
#
# These are the ONLY things that rerun every second.
# They are intentionally isolated from the reading
# passage and the recall text_area, so a tick can
# never blow away in-progress widget state or force
# the passage/textarea to be re-instantiated.
# --------------------------------------------------

@st.fragment(run_every=1)
def reading_timer_fragment():
    # Defensive guard against a known st.fragment(run_every=...) race:
    # the browser-side timer that drives this fragment's auto-ticks is
    # not perfectly synchronized with server-side phase transitions, so
    # a stale tick can still arrive after we've already moved on to the
    # next stage (and popped reading_start_time). Without this guard,
    # that stale tick crashes with an AttributeError. With it, the
    # stale tick is silently ignored instead.
    if (
        st.session_state.get("stage") != "reading"
        or "reading_start_time" not in st.session_state
    ):
        return

    elapsed_time = time.time() - st.session_state.reading_start_time
    total_time = st.session_state.reading_time * 60
    remaining_time = max(0, total_time - elapsed_time)

    remaining_seconds = int(remaining_time)
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

    if remaining_time <= 0:
        _finish_reading()


@st.fragment(run_every=1)
def recall_timer_fragment():
    # Same defensive guard as reading_timer_fragment: ignore stale
    # auto-ticks that arrive after the phase has already moved on
    # (e.g. right after "Submit Recall" pops writing_start_time).
    if (
        st.session_state.get("stage") != "recall"
        or "writing_start_time" not in st.session_state
    ):
        return

    elapsed_time = time.time() - st.session_state.writing_start_time
    total_time = st.session_state.writing_time * 60
    remaining_time = max(0, total_time - elapsed_time)

    remaining_seconds = int(remaining_time)
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    st.info(f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")

    if remaining_time <= 0:
        submit_recall()


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

    if (
        "topic" in st.session_state
        and st.session_state.stage != "setup"
    ):

        st.divider()

        st.caption("Challenge Configuration")

        st.write(
            f"**Topic:** {st.session_state.topic}"
        )

        st.write(
            f"**Difficulty:** {st.session_state.difficulty}"
        )

        st.write(
            f"**Word Limit:** {st.session_state.word_limit}"
        )

        st.write(
            f"**Reading Time:** "
            f"{st.session_state.reading_time} min"
        )

        st.write(
            f"**Writing Time:** "
            f"{st.session_state.writing_time} min"
        )


# --------------------------------------------------
# MAIN CONTENT AREA
# --------------------------------------------------

content_area = st.empty()


with content_area.container():

    # ==================================================
    # SETUP PHASE
    # ==================================================

    if st.session_state.stage == "setup":

        st.title("🧠 Cognify AI")

        st.write(
            "Test how well you can read, remember, "
            "and recall information."
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

                with st.spinner(
                    "Generating your challenge..."
                ):

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
                st.session_state.pop(
                    "reading_start_time",
                    None,
                )

                st.session_state.pop(
                    "writing_start_time",
                    None,
                )

                st.session_state.pop(
                    "recall_text",
                    None,
                )

                st.session_state.pop(
                    "user_recall",
                    None,
                )

                st.session_state.pop(
                    "evaluation_result",
                    None,
                )

                # Start reading timer
                st.session_state.reading_start_time = (
                    time.time()
                )

                st.session_state.stage = "reading"

                content_area.empty()

                st.rerun()


    # ==================================================
    # READING PHASE
    # ==================================================

    elif st.session_state.stage == "reading":

        st.title("📖 Reading Phase")

        # Countdown lives in its own fragment: it is the
        # ONLY thing that reruns every second. The passage
        # below is rendered once per real phase run and is
        # never touched by the 1s tick, so it can no longer
        # flicker or disappear early.
        reading_timer_fragment()

        challenge = st.session_state.challenge

        st.write(
            f"Topic: **{challenge.topic}**"
        )

        st.write(
            f"Difficulty: **{challenge.difficulty}**"
        )

        st.divider()

        # Passage is rendered ONLY in reading phase
        st.write(challenge.content)


    # ==================================================
    # RECALL PHASE
    # ==================================================

    elif st.session_state.stage == "recall":

        st.title("✍️ Recall Phase")

        st.write(
            "The passage has disappeared. "
            "Write everything you remember."
        )

        # Countdown lives in its own fragment. It reruns
        # every second in isolation and, on expiry, saves
        # recall_text -> user_recall and transitions the
        # phase. Because the text_area below sits OUTSIDE
        # this fragment, it is never re-instantiated or
        # resynced by the 1s tick, so typed text can no
        # longer be clobbered mid-keystroke.
        recall_timer_fragment()

        st.text_area(
            "Your Recall",
            placeholder="Write everything you remember...",
            height=300,
            key="recall_text",
        )

        # Keeps recall_text continuously synced to session_state even
        # while the user is mid-keystroke - see _inject_recall_autosync
        # docstring for why this is necessary.
        _inject_recall_autosync()

        # Explicit submit path: lets the user finish recall
        # deterministically without waiting on the timer.
        if st.button("Submit Recall"):
            submit_recall()

    # ==================================================
    # EVALUATION PHASE
    # ==================================================

    elif st.session_state.stage == "evaluation":

        st.title("🔍 Evaluating Your Recall")

        recall_text = st.session_state.get(
            "user_recall",
            "",
        )

        if not recall_text.strip():

            st.error(
                "No recall response was captured."
            )

            st.stop()

        st.info(
            "Analyzing your recall across multiple dimensions..."
        )

        challenge = st.session_state.challenge

        with st.spinner(
            "Running evaluation agents..."
        ):

            result = evaluation_graph.invoke(
                {
                    "original_text": challenge.content,
                    "key_concepts": challenge.key_concepts,
                    "recall_text": recall_text,
                }
            )

        st.session_state.evaluation_result = result
        st.session_state.stage = "result"

        content_area.empty()
        st.rerun()

    # ==================================================
    # RESULT PHASE
    # ==================================================

    elif st.session_state.stage == "result":

        st.title("🏆 Your Recall Result")

        result = (
            st.session_state
            .evaluation_result["final_result"]
        )

        # ----------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------

        st.header(
            f"{result['final_score']:.2f} / 100"
        )

        st.progress(
            result["final_score"] / 100
        )

        st.subheader(
            f"Performance: "
            f"{result['performance_level']}"
        )

        st.divider()

        # ----------------------------------------------
        # STRENGTHS
        # ----------------------------------------------

        st.subheader(
            "What You Remembered Well"
        )

        for point in result["strengths"]:

            st.write(
                f"🟢 {point}"
            )

        # ----------------------------------------------
        # MISSED AREAS
        # ----------------------------------------------

        st.subheader(
            "What You Missed"
        )

        for point in result["missed_areas"]:

            st.write(
                f"🔴 {point}"
            )

        # ----------------------------------------------
        # FEEDBACK
        # ----------------------------------------------

        st.subheader("AI Feedback")

        st.info(
            result["feedback"]
        )

        st.divider()

        # ----------------------------------------------
        # EVALUATION DETAILS
        # ----------------------------------------------

        with st.expander(
            "Evaluation Details"
        ):

            evaluation = (
                st.session_state
                .evaluation_result
            )

            st.write(
                "**Semantic Score:**",
                evaluation[
                    "semantic_result"
                ]["score"],
            )

            st.write(
                "**Coverage Score:**",
                evaluation[
                    "concept_coverage_result"
                ]["score"],
            )

            st.write(
                "**Faithfulness Score:**",
                evaluation[
                    "faithfulness_result"
                ]["score"],
            )

            st.write(
                "**Language Coherence Score:**",
                evaluation[
                    "language_coherence_result"
                ]["overall_score"],
            )

        st.divider()

        # ----------------------------------------------
        # NEW CHALLENGE
        # ----------------------------------------------

        if st.button(
            "Start a New Challenge"
        ):

            for key in list(
                st.session_state.keys()
            ):

                st.session_state.pop(
                    key,
                    None,
                )

            st.session_state.stage = "setup"

            content_area.empty()

            st.rerun()