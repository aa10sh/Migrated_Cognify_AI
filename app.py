import streamlit as st
import time

from agents.content_agent import generate_challenge
from config import (
    APP_NAME,
    WORD_LIMITS,
    DIFFICULTIES,
    READING_TIMES,
    WRITING_TIMES,
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="centered",
)


# Initialize application state
if "stage" not in st.session_state:
    st.session_state.stage = "setup"


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

            st.session_state.stage = "reading"

            st.rerun()


elif st.session_state.stage == "reading":

    st.title("📖 Reading Phase")

    challenge = st.session_state.challenge

    # Initialize timer only once
    if "reading_start_time" not in st.session_state:
        st.session_state.reading_start_time = time.time()

    elapsed_time = (
        time.time()
        - st.session_state.reading_start_time
    )

    total_time = st.session_state.reading_time * 60

    remaining_time = max(
        0,
        total_time - elapsed_time,
    )

    remaining_seconds = int(remaining_time)

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    st.info(
        f"⏱️ Time Remaining: {minutes:02d}:{seconds:02d}"
    )

    # Timer expired
    if remaining_time <= 0:

        # Remove the reading timer
        del st.session_state.reading_start_time

        # Move to recall phase
        st.session_state.stage = "recall"

        st.rerun()

    # Reading content
    st.write(
        f"Topic: **{challenge.topic}**"
    )

    st.write(
        f"Difficulty: **{challenge.difficulty}**"
    )

    st.divider()

    st.write(challenge.content)

    # Refresh every second so timer updates
    time.sleep(1)
    st.rerun()


elif st.session_state.stage == "recall":

    st.title("✍️ Recall Phase")

    st.write(
        "The passage has disappeared. "
        "Write what you remember."
    )

    recall = st.text_area(
        "Your Recall",
        placeholder="Write everything you remember...",
        height=300,
    )

    if st.button("Submit Recall"):

        if not recall.strip():
            st.warning("Please write your recall before submitting.")

        else:
            st.session_state.user_recall = recall

            st.session_state.stage = "evaluation"

            st.rerun()


elif st.session_state.stage == "evaluation":

    st.title("🔍 Evaluation")

    st.write(
        "Your response will be evaluated here."
    )


elif st.session_state.stage == "result":

    st.title("🏆 Result")

    st.write(
        "Your score and feedback will appear here."
    )