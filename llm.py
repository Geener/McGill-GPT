from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
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
        template=qa_template, inpute_variables=["context", "question"]
    )

    llm = OpenAI(temperature=0, max_tokens=1000, model="gpt-3.5-turbo", max_retries=3)

    vectorDB = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=vectorDB.asRetriever(),
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt},
    )


def answer_question(query: str):
    print("Generating response...")

    dqQA = build_llm()

    response = dqQA({"query": query})

    print(response["result"])

    return response
