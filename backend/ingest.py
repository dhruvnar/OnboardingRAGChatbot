from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

def load_documents(path="documents"):
    docs = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".pdf"):
                docs.extend(PyPDFLoader(file_path).load())
            elif file.endswith(".docx"):
                docs.extend(Docx2txtLoader(file_path).load())
            elif file.endswith(".txt"):
                docs.extend(TextLoader(file_path).load())
    return docs

def ingest_documents():
    raw_docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=500)
    chunks = splitter.split_documents(raw_docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embeddings)
    vectordb.save_local("vector_store")
    print("Local vector store created successfully.")

if __name__ == "__main__":
    ingest_documents()