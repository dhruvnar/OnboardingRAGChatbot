from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from pinecone import Pinecone as PineconeClient, ServerlessSpec
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

    embeddings = OpenAIEmbeddings()

    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    pinecone_cloud = os.getenv("PINECONE_CLOUD")
    pinecone_region = os.getenv("PINECONE_REGION")

    if not all([pinecone_api_key, pinecone_index_name, pinecone_cloud, pinecone_region]):
        raise ValueError("PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_CLOUD, and PINECONE_REGION must be set in the .env file")

    pinecone = PineconeClient(api_key=pinecone_api_key)

    if pinecone_index_name not in pinecone.list_indexes().names():
        pinecone.create_index(
            name=pinecone_index_name,
            dimension=1536, # Dimension for text-embedding-ada-002
            metric="cosine",
            spec=ServerlessSpec(
                cloud=pinecone_cloud,
                region=pinecone_region
            )
        )

    Pinecone.from_documents(chunks, embeddings, index_name=pinecone_index_name)


if __name__ == "__main__":
    ingest_documents()