from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

def create_vectorDB():
    print("Creating your vectorDB...")
    
    my_loader = DirectoryLoader('output/', glob='*.txt')
    documents = my_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 700, chunk_overlap = 0)
    docs = text_splitter.split_documents(documents)

    vectorDB = FAISS.from_documents(docs, OpenAIEmbeddings())
    vectorDB.save_local('vectorDB/db_faiss')

    print("VectorDB created.")

if __name__ == '__main__':
    create_vectorDB()