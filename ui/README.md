<<<<<<< HEAD
# AI Tax Assistant

An AI-powered Tax & Legal Assistant built using React, FastAPI, Ollama, and RAG (Retrieval-Augmented Generation).

## Features

* AI chatbot for tax and legal questions
* OCR support for image-based queries
* RAG-based accurate responses
* Offline local LLM support using Ollama
* React frontend + FastAPI backend
* Voice input support
* Image analysis support

---

## Tech Stack

### Frontend

* React.js
* CSS
* Axios

### Backend

* FastAPI
* Python
* Ollama
* LangChain

### AI Models

* llama3.2
* llava

---

## Project Structure

```bash
frontend/
backend/
knowledge_base/
uploads/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Isha311219/RAG_Agentic_aI.git
cd RAG_Agentic_aI
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

---

## Features in Detail

### Tax Question Answering

Ask questions related to:

* GST
* Income Tax
* Deductions
* Tax Regimes
* Legal Rights

### OCR + Image Analysis

Upload screenshots or documents and extract questions automatically.

### RAG Accuracy

Uses a curated knowledge base to reduce hallucinations and improve response accuracy.

---

## Future Improvements

* PDF analysis
* Multilingual support
* Better legal reasoning
* Cloud deployment
* Authentication system

---


=======
AI Tax Assistant
An AI-powered Tax & Legal Assistant built using React, FastAPI, Ollama, and RAG (Retrieval-Augmented Generation).

Features
AI chatbot for tax and legal questions
OCR support for image-based queries
RAG-based accurate responses
Offline local LLM support using Ollama
React frontend + FastAPI backend
Voice input support
Image analysis support
Tech Stack
Frontend
React.js
CSS
Axios
Backend
FastAPI
Python
Ollama
LangChain
AI Models
llama3.2
llava
Project Structure
frontend/
backend/
knowledge_base/
uploads/
Installation
Clone Repository
git clone https://github.com/Isha311219/RAG_Agentic_aI.git
cd RAG_Agentic_aI
Backend Setup
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
Backend runs on:

http://127.0.0.1:8000
Frontend Setup
cd frontend

npm install

npm start
Frontend runs on:

http://localhost:3000
Features in Detail
Tax Question Answering
Ask questions related to:

GST
Income Tax
Deductions
Tax Regimes
Legal Rights
OCR + Image Analysis
Upload screenshots or documents and extract questions automatically.

RAG Accuracy
Uses a curated knowledge base to reduce hallucinations and improve response accuracy.

Future Improvements
PDF analysis
Multilingual support
Better legal reasoning
Cloud deployment
Authentication system
>>>>>>> 0e36b67 (fix: apply gitignore and clean tracked files)
