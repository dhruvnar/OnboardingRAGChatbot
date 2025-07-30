from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from chatbot import answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def ask(q: str = Query(..., description="Question")):
    answer = answer_question(q)
    return {"answer": answer}