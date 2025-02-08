import streamlit as st
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client with API key from environment variable
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Initialize session state
def init_session_state():
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'wrong_attempts' not in st.session_state:
        st.session_state.wrong_attempts = 0
    if 'highest_level' not in st.session_state:
        st.session_state.highest_level = 1

# AI question generation
def generate_question(level):
    difficulty = "basic" if level <= 3 else "intermediate" if level <= 6 else "advanced"
    
    prompt = f"""Generate a {difficulty} multiple-choice question about space exploration, Mars, or astronomy.
    The response should be in this exact JSON format:
    {{
        "question": "The question text here",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_index": 0,
        "explanation": "Detailed explanation why this is correct"
    }}
    Make sure the difficulty matches level {level}."""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)

def main():
    # Check if API key is set
    if not os.getenv('GROQ_API_KEY'):
        st.error("Please set your GROQ_API_KEY environment variable before running the app.")
        st.stop()
    
    # Initialize session state
    init_session_state()
    
    st.title("🚀 Space Explorer Quiz")
    st.markdown("Test your knowledge of space, Mars, and astronomy!")
    
    # Show current level and progress
    st.header(f"Level {st.session_state.level}")
    st.progress(min(st.session_state.level / 10, 1.0))
    
    # Start Quiz button
    if 'quiz_started' not in st.session_state:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        # Generate and display question
        if not st.session_state.current_question:
            with st.spinner("Generating question..."):
                st.session_state.current_question = generate_question(st.session_state.level)
        
        # Display question
        st.markdown(f"""
        <div class='question-box'>
            <h3>{st.session_state.current_question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Display options
        selected_option = st.radio(
            "Select your answer:", 
            st.session_state.current_question['options'],
            key=f"question_{st.session_state.level}"
        )
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Submit Answer"):
                correct_index = st.session_state.current_question['correct_index']
                if selected_option == st.session_state.current_question['options'][correct_index]:
                    st.success("🎉 Correct! Moving to next level!")
                    st.session_state.level += 1
                    st.session_state.wrong_attempts = 0
                    st.session_state.current_question = None
                    st.session_state.highest_level = max(st.session_state.highest_level, st.session_state.level)
                    st.rerun()
                else:
                    st.session_state.wrong_attempts += 1
                    st.error("❌ Incorrect! Try again!")
                    if st.session_state.wrong_attempts >= 2:
                        st.markdown(f"💡 **Hint:** {st.session_state.current_question['explanation']}")
        
        with col2:
            if st.button("Start Over"):
                st.session_state.level = 1
                st.session_state.current_question = None
                st.session_state.wrong_attempts = 0
                st.session_state.quiz_started = False
                st.rerun()

if __name__ == "__main__":
    main()