import streamlit as st
from groq import Groq
import json
import os
from dotenv import load_dotenv
import random
import time

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
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()

# Custom CSS for better styling
def load_custom_css():
    st.markdown("""
        <style>
        .question-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f8ff;
            margin: 20px 0;
            border: 2px solid #4169e1;
        }
        .achievement-unlocked {
            padding: 10px;
            background-color: #ffd700;
            border-radius: 5px;
            color: #000;
            text-align: center;
            animation: glow 1s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
                box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ffd700;
            }
            to {
                box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ffd700;
            }
        }
        .streak-counter {
            font-size: 24px;
            font-weight: bold;
            color: #ff4b4b;
        }
        </style>
    """, unsafe_allow_html=True)

# Achievement system
ACHIEVEMENTS = {
    'First Step': 'Complete your first question',
    'Quick Learner': 'Get 3 correct answers in a row',
    'Space Expert': 'Reach level 5',
    'Perfect Round': 'Complete a level without wrong attempts',
    'Marathon Runner': 'Answer 10 questions total'
}

def check_achievements():
    new_achievements = []
    
    if st.session_state.total_questions == 1:
        new_achievements.append('First Step')
    if st.session_state.streak >= 3:
        new_achievements.append('Quick Learner')
    if st.session_state.level >= 5:
        new_achievements.append('Space Expert')
    if st.session_state.wrong_attempts == 0:
        new_achievements.append('Perfect Round')
    if st.session_state.total_questions >= 10:
        new_achievements.append('Marathon Runner')
    
    for achievement in new_achievements:
        if achievement not in st.session_state.achievements:
            st.session_state.achievements.add(achievement)
            st.markdown(f"""
                <div class='achievement-unlocked'>
                    🏆 Achievement Unlocked: {achievement}!
                    <br>{ACHIEVEMENTS[achievement]}
                </div>
            """, unsafe_allow_html=True)

def generate_question(level):
    difficulty = "basic" if level <= 3 else "intermediate" if level <= 6 else "advanced"
    
    prompt = f"""Generate a {difficulty} multiple-choice question about space exploration, Mars, or astronomy.
    The response should be in this exact JSON format:
    {{
        "question": "The question text here",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_index": 0,
        "explanation": "Detailed explanation why this is correct",
        "fun_fact": "An interesting related fact about this topic"
    }}
    Make sure the difficulty matches level {level}."""

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)

def celebrate_correct_answer():
    st.balloons()
    st.success("🎉 Correct! Moving to next level!")
    messages = [
        "Amazing work, Space Cadet! 🌟",
        "You're a Cosmic Genius! 🚀",
        "Keep reaching for the stars! ⭐",
        "Astronomical knowledge! 🌍",
        "Out of this world! 🌌"
    ]
    st.markdown(f"### {messages[st.session_state.level % len(messages)]}")

def main():
    load_custom_css()
    
    if not os.getenv('GROQ_API_KEY'):
        st.error("Please set your GROQ_API_KEY environment variable before running the app.")
        st.stop()
    
    init_session_state()
    
    # Welcome screen and username input
    if not st.session_state.username:
        st.title("🌌 Welcome to Space Explorer Quiz!")
        st.markdown("""
            Embark on an incredible journey through space! Test your knowledge of astronomy, 
            space exploration, and the mysteries of the cosmos.
        """)
        username = st.text_input("Enter your space explorer name:")
        if username:
            st.session_state.username = username
            st.balloons()
            st.success(f"Welcome aboard, Space Explorer {username}! 🚀")
            time.sleep(1)
            st.rerun()
    
    else:
        st.title(f"🚀 Space Explorer Quiz - Navigator {st.session_state.username}")
        
        # Sidebar with stats
        with st.sidebar:
            st.markdown("### 📊 Mission Stats")
            st.markdown(f"🏆 Highest Level: {st.session_state.highest_level}")
            st.markdown(f"📈 Current Score: {st.session_state.score}")
            st.markdown(f"🔥 Current Streak: {st.session_state.streak}")
            st.markdown(f"📝 Total Questions: {st.session_state.total_questions}")
            
            st.markdown("### 🏅 Achievements")
            for achievement in st.session_state.achievements:
                st.markdown(f"- {achievement}")
        
        # Main quiz interface
        st.header(f"Level {st.session_state.level}")
        progress = min(st.session_state.level / 10, 1.0)
        st.progress(progress, text=f"Mission Progress: {int(progress * 100)}%")
        
        if 'quiz_started' not in st.session_state:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🚀 Launch Mission", use_container_width=True):
                    st.session_state.quiz_started = True
                    st.rerun()
        else:
            if not st.session_state.current_question:
                with st.spinner("Preparing next challenge..."):
                    st.session_state.current_question = generate_question(st.session_state.level)
            
            st.markdown(f"""
            <div class='question-box'>
                <h3>{st.session_state.current_question['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            selected_option = st.radio(
                "Select your answer:", 
                st.session_state.current_question['options'],
                key=f"question_{st.session_state.level}"
            )
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🚀 Submit Answer", use_container_width=True):
                    correct_index = st.session_state.current_question['correct_index']
                    if selected_option == st.session_state.current_question['options'][correct_index]:
                        celebrate_correct_answer()
                        st.session_state.level += 1
                        st.session_state.score += (10 - st.session_state.wrong_attempts)
                        st.session_state.streak += 1
                        st.session_state.total_questions += 1
                        st.session_state.current_question = None
                        st.session_state.highest_level = max(st.session_state.highest_level, st.session_state.level)
                        check_achievements()
                        
                        # Show fun fact
                        st.info(f"🌟 Fun Fact: {st.session_state.current_question['fun_fact']}")
                        
                        st.rerun()
                    else:
                        st.session_state.wrong_attempts += 1
                        st.session_state.streak = 0
                        st.error("❌ Not quite right! Try again!")
                        if st.session_state.wrong_attempts >= 2:
                            st.markdown(f"💡 **Hint:** {st.session_state.current_question['explanation']}")
            
            with col2:
                if st.button("🔄 Start New Mission", use_container_width=True):
                    for key in ['level', 'current_question', 'wrong_attempts', 'quiz_started', 'score', 'streak']:
                        if key in st.session_state:
                            st.session_state[key] = 0
                    st.session_state.level = 1
                    st.rerun()

if __name__ == "__main__":
    main()
