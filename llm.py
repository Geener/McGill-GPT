from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.llms import OpenAI


qa_template = """Use the following pieces of information to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Context: {context}
Question: {question}
Only return the helpful answer below and nothing else.
Helpful answer:
"""


def build_llm():
    prompt = PromptTemplate(
        template=qa_template, input_variables=["context", "question"]
    )

    llm = OpenAI(
        temperature=0, max_tokens=1000, model="text-davinci-003", max_retries=3
    )
    vectorDB = FAISS.load_local("vectorDB/db_faiss", OpenAIEmbeddings())

    # dbqa = RetrievalQA.from_chain_type(
    #     llm,
    #     chain_type="stuff",
    #     retriever=vectorDB.as_retriever(),
    #     return_source_documents=True,
    #     chain_type_kwargs={"prompt": prompt},
    # )

    dbqa_history = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorDB.as_retriever(),
        chain_type="stuff",
        return_source_documents=True,
    )

    return dbqa_history


def answer_question(query: str, chat_history):
    print("Generating response...")

    dqQA = build_llm()

    response = dqQA({"question": query, "chat_history": chat_history})

    print(response)

    return response
