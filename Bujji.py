import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from streamlit_chat import message

# Specify the PDF file path
pdf_path = 'mental_health_Document.pdf'

# Initialize session state
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

# Function to handle conversation
def conversation_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

# Function to display chat history
def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your Mental Health", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversation_chat(user_input)

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state['generated'][i], key=str(i), avatar_style="fun-emoji")

# Check if the PDF file exists and load it
if os.path.exists(pdf_path):
    try:
        # Load the PDF file
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_documents(documents)

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                           model_kwargs={'device': "cpu"})

        # Create vector store
        vector_store = FAISS.from_documents(text_chunks, embeddings)

        # Create LLM
        llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin", model_type="llama",
                            config={'max_new_tokens': 128, 'temperature': 0.01})

        # Set up memory for conversation
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Create conversational chain
        chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                      retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                      memory=memory)

        st.title("HealthCare ChatBot 🧑🏽‍⚕️")
        
        # Initialize session state
        initialize_session_state()
        
        # Display chat history
        display_chat_history()

    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
else:
    st.error("The specified PDF file does not exist.")
