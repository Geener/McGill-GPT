import streamlit as st
from dotenv import load_dotenv
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

    if "I'm sorry" in answer:
        return answer

    sources_list = list(sources)
    sources_list.sort()
    display_sources = "Sources:\n"

    for index, source in enumerate(sources):
        display_sources += f"{index+1}. {format_source(source)} \n"

    return answer + "\n\n" + display_sources


st.title("💬 McGill GPT")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "result": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["result"])

if question := st.chat_input():
    st.session_state.messages.append({"role": "user", "result": question})
    st.chat_message("user").write(question)

    response = answer_question(query=question)

    base_answer = response["result"]
    sources = set(doc.metadata["source"] for doc in response["source_documents"])

    formatted_response = display_answer(base_answer, sources)
    st.session_state.messages.append(
        {"role": "assistant", "result": formatted_response}
    )
    st.chat_message("assistant").write(formatted_response)
