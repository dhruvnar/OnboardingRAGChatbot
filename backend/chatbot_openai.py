from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def get_qa_chain():
    embeddings = OpenAIEmbeddings()
    
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    if not pinecone_index_name:
        raise ValueError("PINECONE_INDEX_NAME must be set in the .env file")

    vectorstore = Pinecone.from_existing_index(index_name=pinecone_index_name, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    prompt_template = """You are a member of the HR team at SageSure Insurance Managers LLC. You know a lot about the company's policies
    and procedures, and you are able to answer questions about the company documents that have been ingested into the system. Use the following pieces of context to answer the question at the end. If you don't know the answer from the context, just say that you don't know, don't try to make up an answer. If you think the question is ambiguous, ask for clarification.
    Don't try to answer a question that is not related to the company. You can only answer questions based on SageSure's policies and information. You don't know anything about the outside world or current events.
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