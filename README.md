# Onboarding HR Chatbot

This is a retrieval-augmented generation (RAG) chatbot designed to answer questions about internal company HR documents. It uses a fully local setup with Ollama and Hugging Face embeddings to ensure all company data remains private and secure. The frontend is a modern, responsive web application built with React.

![Chatbot UI](./frontend/public/screenshot.png) <!-- You can add a screenshot of the app here -->

## Features

-   **Local & Private:** All AI processing and data storage is done on your local machine. No data is sent to third-party APIs.
-   **Multi-Format Document Ingestion:** Supports ingesting `.pdf`, `.docx`, and `.txt` files.
-   **Custom LLM Prompts:** The language model is guided by a carefully crafted system prompt to ensure it acts as a helpful, accurate HR assistant.
-   **Modern Conversational UI:** A beautiful, app-style interface for interacting with the chatbot.
    -   Professional dark theme with themed green accents.
    -   Multi-panel layout with a sidebar for chat history.
    -   "Typing..." indicator and message timestamps for a realistic feel.
    -   Clickable example prompts to help users get started.

## Tech Stack

-   **Backend:** Python, FastAPI, LangChain
-   **AI & ML:** Open AI LLM, Open AI Embeddings, Pinecone Vector Store
-   **Frontend:** React, JavaScript (ES6+), CSS3
-   **Tooling:** Uvicorn (ASGI Server), npm (Node Package Manager)

## Prerequisites

Before you begin, ensure you have the following installed on your system:
-   [Python](https://www.python.org/downloads/) (3.9 or higher)
-   [Node.js and npm](https://nodejs.org/en/download/) (LTS version recommended)
-   [Ollama](https://ollama.com/) installed and running on your machine.

---

## Setup and Installation

Follow these steps to get the project up and running.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd P02OnboardingChatBot
```

### 2. Configure the Backend

From the project root directory (`P02OnboardingChatBot`), set up the Python environment.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .\\.venv\\Scripts\\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure the Frontend

In a new terminal, navigate to the `frontend` directory and install the necessary Node.js packages.

```bash
cd frontend
npm install
```

### 4. Set Up the Local LLM

Make sure the Ollama application is running on your desktop. Then, pull the model used by the chatbot (the default is `llama3`).

```bash
ollama pull llama3
```

---

## How to Use

### 1. Add Your Documents

Place all your company's HR documents (e.g., employee handbooks, policy PDFs) inside the `backend/documents/` directory.

### 2. Ingest Your Data

Before running the app for the first time, you must run the ingestion script. This will read your documents, create embeddings, and build a local vector database.

From the **project root directory**, run:
```bash
python backend/ingest.py
```
This command only needs to be run once, or whenever you add, remove, or change the documents in the `documents` folder.

### 3. Run the Application

You will need two separate terminals to run both the backend and frontend servers.

**Terminal 1: Start the Backend Server**
From the **project root directory**:
```bash
uvicorn backend.main:app --reload
```
The backend will be available at `http://localhost:8000`.

**Terminal 2: Start the Frontend Application**
From the **`frontend` directory**:
```bash
npm start
```
The React application will open automatically in your browser at `http://localhost:3000`.

---

## Project Structure
