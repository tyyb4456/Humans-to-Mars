import streamlit as st
import time
import json
from datetime import datetime
import os
from groq import Groq
from dotenv import load_dotenv
#from utils import create_sidebar

load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv('GROQ_API_KEY')
)

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
            "content": "You are an expert on Mars and space exploration. Provide accurate, informative responses about Mars, its features, exploration missions, and related topics. Keep responses concise but informative."
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
            model= "llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response from Groq: {str(e)}")
        return "I apologize, but I'm having trouble generating a response right now. Please try again."

def chat_interface():
    st.title("Mars Expert AI Chatbot")
    st.write("Ask me anything about Mars! I'm here to help you learn about the Red Planet.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about Mars..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_groq_response(st.session_state.messages)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    #create_sidebar()
    chat_interface()

if __name__ == "__main__":
    main()
