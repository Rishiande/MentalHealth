# Import necessary libraries
import streamlit as st
import google.generativeai as genai

# Install Google Generative AI SDK (Uncomment if needed)
# !pip install -q -U google-generativeai

# Directly set your API key
API_KEY = "AIzaSyDKUpdDE-WBhOVFTdRTVYncxyG1MFCpUWs"

# Configure the generative AI client with your API key
genai.configure(api_key=API_KEY)

# Create the Generative Model using the specified model name
model = genai.GenerativeModel('gemini-pro')

# Function to get a response from the Generative AI model
def get_response_gemini(user_input):
    try:
        # Generate content based on the user's input
        response = model.generate_content(user_input)
        # Extract the generated response text
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main function to run the Streamlit app
def main():
    st.title("Mental Health Chatbot")
    st.write("This is a mental health chatbot. Feel free to share your thoughts.")
    
    # Input from the user
    user_input = st.text_input("You:")
    
    if user_input:
        # Get the response from the Generative AI model
        response = get_response_gemini(user_input)
        
        # Display the bot's response
        st.write("Bot:", response)

# Run the app
if __name__ == "__main__":
    main()
