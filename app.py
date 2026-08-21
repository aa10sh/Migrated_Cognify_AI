import streamlit as st
from agents.content_agent import generate_challenge
from config import (
    APP_NAME,
    WORD_LIMITS,
    DIFFICULTIES,
    READING_TIMES,
    WRITING_TIMES,
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
            st.session_state.topic = topic
            st.session_state.word_limit = word_limit
            st.session_state.difficulty = difficulty
            st.session_state.reading_time = reading_time
            st.session_state.writing_time = writing_time

            st.session_state.stage = "reading"

            st.rerun()


elif st.session_state.stage == "reading":

    st.title("📖 Reading Phase")

    st.info(
        "The generated passage will appear here."
    )

    st.write(
        f"Topic: **{st.session_state.topic}**"
    )

    st.write(
        f"Difficulty: **{st.session_state.difficulty}**"
    )

    st.write(
        f"Reading Time: **{st.session_state.reading_time} minutes**"
    )


elif st.session_state.stage == "recall":

    st.title("✍️ Recall Phase")

    st.write(
        "The passage has disappeared. "
        "Write what you remember."
    )


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




st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="centered",
)




