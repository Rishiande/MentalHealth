import os
import streamlit as st
import google.generativeai as genai
from streamlit_chat import message

# Set the Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyDKUpdDE-WBhOVFTdRTVYncxyG1MFCpUWs"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Title of the Streamlit app
st.markdown("<h1 style='text-align: center;'>🩺 HealthCare ChatBot</h1>", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about mental health 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

# Function to handle conversation using Google Generative AI
def conversation_chat(query):
    # Create a Generative Model instance
    model = genai.GenerativeModel('gemini-pro')
    
    # Generate content based on user input
    response = model.generate_content(query)
    
    # Append query and response to session history
    st.session_state['history'].append((query, response.text))
    return response.text

# Function to display chat history
def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        # Input form for user queries
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your mental health", key='input')
            submit_button = st.form_submit_button(label='Send')

        # If submit button is pressed and there's user input
        if submit_button and user_input:
            # Get chatbot response
            output = conversation_chat(user_input)

            # Append user input and output to session state
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    # Display chat history
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                # Display user input and chatbot response in conversation bubbles
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state['generated'][i], key=str(i), avatar_style="fun-emoji")

# Main part of the Streamlit app
# Initialize session state
initialize_session_state()

# Display chat history and input form
display_chat_history()
