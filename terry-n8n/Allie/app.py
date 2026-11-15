import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Allie - Mortgage Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        padding: 12px;
        border-radius: 8px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        background-color: #4f46e5;
        color: white;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #4338ca;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #eef2ff;
        margin-left: 20%;
    }
    .chat-message.assistant {
        background-color: #f3f4f6;
        margin-right: 20%;
    }
    .source {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm Allie, your mortgage assistant. How can I help you with your mortgage questions today?",
            "timestamp": datetime.now().isoformat()
        }
    ]

# Sidebar for additional controls
with st.sidebar:
    st.title("Allie Settings")
    st.markdown("---")
    
    # Theme selection
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark", "System"],
        index=2
    )
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi there! I'm Allie, your mortgage assistant. How can I help you with your mortgage questions today?",
                "timestamp": datetime.now().isoformat()
            }
        ]
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Allie is your AI-powered mortgage assistant, here to help with all your mortgage-related questions.")
    st.markdown("---")
    st.markdown("*Powered by n8n & Streamlit*")

# Main chat interface
def send_message():
    if st.session_state.user_input.strip() == "":
        return
    
    # Add user message to chat
    user_message = {
        "role": "user",
        "content": st.session_state.user_input,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    # Show typing indicator
    with st.spinner("Allie is thinking..."):
        try:
            # Call n8n webhook
            response = requests.post(
                "https://tshelton.app.n8n.cloud/webhook/ba394493-d92a-4ec4-b493-ea237bffa2aa",
                json={"message": st.session_state.user_input}
            )
            
            if response.status_code == 200:
                if not response.text.strip():
                    raise Exception("Received empty response from the server")
                    
                data = response.json()
                if not hasattr(data, 'output'):
                    raise Exception("Response does not contain 'output' field")
                    
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data.output,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                raise Exception(f"API request failed with status {response.status_code}")
                
        except Exception as e:
            error_msg = f"Sorry, I couldn't get a response from Allie. Please try again later."
            if 'response' in locals():
                error_msg += f"\n\nDebug info:"
                error_msg += f"\nStatus: {response.status_code}"
                error_msg += f"\nContent-Type: {response.headers.get('Content-Type', 'N/A')}"
                error_msg += f"\nResponse length: {len(response.text)} bytes"
                
                if response.text.strip():
                    error_msg += f"\nResponse start: {response.text[:200]}..."
                
            print(f"Error: {str(e)}\n{error_msg}")
            st.error(error_msg)
    
    # Clear input after sending
    st.session_state.user_input = ""

# Display chat messages
st.title("Allie - Mortgage Assistant")

# Chat container
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("source"):
                st.caption(f"Source: {msg['source']}")

# Input area
st.text_input(
    "Type your message...",
    key="user_input",
    on_change=send_message,
    label_visibility="collapsed"
)

# Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
