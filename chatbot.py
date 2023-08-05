import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
from llm import answer_question

load_dotenv()


# Removes "\output", replaces _ with \, removes ".txt"
def format_source(input_string: str) -> str:
    # Remove "output/" from the beginning of the string
    if input_string.startswith("output\\"):
        input_string = input_string[len("output\\") :]

    # Remove ".txt" at the end of the string
    if input_string.endswith(".txt"):
        input_string = input_string[: -len(".txt")]

    # Change all "_" to "/"
    input_string = input_string.replace("_", "/")

    return input_string


# combines answer and sources
def display_answer(answer: str, sources) -> str:
    # if no sources were found
    if not sources:
        return ""

    sources_list = list(sources)
    sources_list.sort()
    display_sources = "Sources:\n"

    for index, source in enumerate(sources):
        display_sources += f"{index+1}. {format_source(source)} \n"

    return answer + "\n\n" + display_sources


st.header("💬 McGill Chatbot")

# Creates text input
question = st.text_input("Question", placeholder="Enter your question here...")

# initialize both lists to empty (since no chat history)
if "user_question_history" not in st.session_state:
    st.session_state["user_question_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

# Generates and displays query response when entered
if question:
    with st.spinner("Generating response..."):
        response = answer_question(query=question)

        question = response["query"]
        base_answer = response["result"]
        sources = set(doc.metadata["source"] for doc in response["source_documents"])

        formatted_response = display_answer(base_answer, sources)

        st.session_state["user_question_history"].append(question)
        st.session_state["chat_answers_history"].append(formatted_response)


# Display messages in chat format
if st.session_state["chat_answers_history"]:
    for answer, question in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_question_history"],
    ):
        message(question, is_user=True, key=question)
        message(answer, key=answer)
