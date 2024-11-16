import os
import streamlit as st
import google.generativeai as genai

# Set the Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCWmWlwM4R3Otqp0Go51z9EVCNfEgWa2rM"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Create a Generative Model instance
model = genai.GenerativeModel('gemini-pro')

# Title of the Streamlit app
st.title("Mental Health Chatbot")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for user query
if prompt := st.chat_input("Ask me anything about mental health (e.g., 'What are some coping strategies for anxiety?')"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate content based on user input
    response = model.generate_content(prompt)
    
    # Display assistant response in the chat
    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response.text})
