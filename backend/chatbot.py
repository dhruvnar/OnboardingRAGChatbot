from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_qa_chain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load the local FAISS vector store
    vectordb = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    
    # Use Ollama as the local language model
    llm = Ollama(model="llama3", base_url="http://localhost:11434")

    prompt_template = """You are a helpful assistant for answering questions about company documents.
Use the following pieces of context to answer the question at the end.
If you don't know the answer from the context, just say that you don't know, don't try to make up an answer.
If you think the question is ambiguous, ask for clarification. Just give the answer, don't say 'based on the context' or
anything like that. The user only cares about the answer and it's details.

Context: {context}

Question: {question}

Helpful Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs
    )

def answer_question(query):
    qa = get_qa_chain()
    response = qa.invoke({"query": query})
    return response.get("result", "Sorry, I couldn't find an answer.")
