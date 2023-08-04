from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate


def build_llm(query: str) -> Any:
    # embeddings = OpenAIEmbeddings()

    # docsearch = FAISS.from

    prompt = PromptTemplate(
        template=qa_template, inpute_variables=['context', 'question']
    )