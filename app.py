import streamlit as st
import random
import json

# Load questions from a JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Initialize session state for the game
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False

def start_game():
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.game_started = True
    st.session_state.current_questions = random.sample(questions, len(questions)) # Shuffle questions
    st.session_state.answer_submitted = False

def reset_game():
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.game_started = False
    st.session_state.current_questions = []
    st.session_state.answer_submitted = False

st.title("Geography Quiz Game")
st.write("Test your knowledge about geography and related aspects!")

if not st.session_state.game_started:
    st.button("Start Game", on_click=start_game)
else:
    st.sidebar.button("Reset Game", on_click=reset_game)

    if st.session_state.question_index < len(st.session_state.current_questions):
        current_question_data = st.session_state.current_questions[st.session_state.question_index]
        st.subheader(f"Category: {current_question_data['category']}")
        st.write(f"Question: {current_question_data['question']}")

        user_answer = st.radio(
            "Is this statement true?",
            ("True", "False"),
            key=f"question_{st.session_state.question_index}"
        )

        if st.button("Submit Answer", disabled=st.session_state.answer_submitted):
            correct_answer_str = "True" if current_question_data["answer"] else "False"
            if user_answer == correct_answer_str:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. The correct answer was {current_question_data['answer']}.")
            st.session_state.answer_submitted = True
            # st.rerun()

        if st.session_state.answer_submitted:
            if st.button("Next Question"):
                st.session_state.question_index += 1
                st.session_state.answer_submitted = False
                st.rerun()

    else:
        st.success(f"Game Over! You scored {st.session_state.score} out of {len(questions)}.")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Play Again", on_click=start_game)
        with col2:
            if st.button("Exit"):
                st.stop()

st.sidebar.write(f"Current Score: {st.session_state.score}")
