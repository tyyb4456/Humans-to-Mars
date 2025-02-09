import streamlit as st
import time
import json
from datetime import datetime
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)

# Default questions to help users get started
DEFAULT_QUESTIONS = [
    "What is the average temperature on Mars?",
    "Tell me about the Mars rovers currently operating",
    "How long would it take to travel to Mars?",
    "What makes Mars' atmosphere different from Earth's?",
    "What evidence is there for water on Mars?",
]

# Enhanced system prompt
SYSTEM_PROMPT = """You are an expert AI assistant specializing in Mars and space exploration, with deep knowledge of:
- Mars' physical characteristics, geology, and atmosphere
- Past, present, and planned Mars exploration missions
- Potential for human colonization and terraforming
- Scientific discoveries and research about Mars
- Comparison between Mars and Earth
- Technical aspects of Mars exploration technology

Provide accurate, well-structured responses that:
- Use clear, accessible language while maintaining scientific accuracy
- Include relevant facts and figures when appropriate
- Address both historical context and current developments
- Acknowledge areas of scientific uncertainty
- Stay focused on Mars-related topics
- Keep responses concise but informative
"""

def load_chat_history():
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    with open("chat_history.json", "w") as f:
        json.dump(history, f)

def get_groq_response(messages):
    """
    Get response from Groq API
    """
    try:
        # Convert chat history to Groq format
        formatted_messages = []
        system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
        formatted_messages.append(system_message)
        
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=formatted_messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response from Groq: {str(e)}")
        return "I apologize, but I'm having trouble generating a response right now. Please try again."

def chat_interface():
    st.title("Mars Expert AI Chatbot 🚀")
    st.write("Ask me anything about Mars! I'm here to help you learn about the Red Planet.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Create two columns - one for chat and one for questions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # # Add clear chat button
        # if st.button("Clear Chat"):
        #     st.session_state.messages = []
        #     st.experimental_rerun()
        
        # Chat input
        if prompt := st.chat_input("Ask a question about Mars..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking about Mars..."):
                    response = get_groq_response(st.session_state.messages)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        # Example questions section
        st.markdown("### Try these questions:")
        for question in DEFAULT_QUESTIONS:
            if st.button(question, key=f"btn_{question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                with chat_container.chat_message("user"):
                    st.markdown(question)
                
                with chat_container.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = get_groq_response(st.session_state.messages)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    chat_interface()

if __name__ == "__main__":
    main()
