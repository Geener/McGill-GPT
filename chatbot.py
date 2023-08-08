import streamlit as st
from dotenv import load_dotenv
from llm import answer_question

load_dotenv()


# Load the image
mcgill_path = "images/McGill-crest.jpg"  # Replace with your image filename
banner_path = "images/McGill-banner.png"
emoji_path = "images/student_emoji.png"


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

    if "I'm sorry" in answer:
        return answer

    sources_list = list(sources)
    sources_list.sort()
    display_sources = "Sources:\n"

    for index, source in enumerate(sources):
        display_sources += f"{index+1}. {format_source(source)} \n"

    return answer + "\n\n" + display_sources


st.image(banner_path)
st.caption(
    """Ask any McGill related question to get up to date instant answers.  \nNot affiliated with McGill.  \nBy: Adam Geenen"""
)

# Creates default chatbot message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "McGill", "result": "How can I help you?"}]

# Used to store chat history and pass it back to the LLM
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Determine what icon to use for chat based on role
for msg in st.session_state.messages:
    if msg["role"] == "McGill":
        st.chat_message(msg["role"], avatar=mcgill_path).write(msg["result"])
    else:
        st.chat_message(msg["role"], avatar=emoji_path).write(msg["result"])

#
if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "result": question})
    st.chat_message("user", avatar=emoji_path).write(question)

    response = answer_question(
        query=question, chat_history=st.session_state["chat_history"]
    )

    base_answer = response["answer"]
    sources = set(doc.metadata["source"] for doc in response["source_documents"])

    formatted_response = display_answer(base_answer, sources)
    st.session_state["messages"].append(
        {"role": "McGill", "result": formatted_response}
    )
    st.chat_message("McGill", avatar=mcgill_path).write(formatted_response)

    st.session_state["chat_history"].append((question, base_answer))
