import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
from llm import answer_question

load_dotenv()

st.header("💬 McGill Chatbot")

question = st.text_input("Question", placeholder="Enter your question here...")

if question:
    with st.spinner("Generating response..."):
        response = answer_question(query=question)
        st.write(response)
        print(response)
