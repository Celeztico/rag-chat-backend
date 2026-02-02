# 📄 RAG Backend – PDF-based Question Answering

This is a **backend-only learning project** that implements a **Retrieval-Augmented Generation (RAG)** system.

The backend:
- accepts **PDF uploads**
- extracts and embeds their content
- stores embeddings in a **local vector database**
- answers user questions **grounded in the uploaded PDFs** using an LLM

This project is intentionally kept simple and is meant for **learning, experimentation, and short-term hosting**.

---

## ✨ Features (Current Phase)

- Upload text-based PDF files
- Extract and chunk PDF content
- Generate embeddings locally
- Store embeddings in a local vector database
- Retrieve relevant context for a question
- Generate answers using **Groq LLM**
- Simple REST API (no frontend)

> ⚠️ User authentication, multi-chat support, and deployment controls are planned for later phases.

---

## 🧠 Tech Stack

### Backend
- **Python 3**
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI server

### RAG Pipeline
- **PyPDF** – PDF text extraction
- **Sentence-Transformers** – local embeddings (`all-MiniLM-L6-v2`)
- **ChromaDB (local)** – vector database
- **Groq API** – LLM for answering questions

### Utilities
- **python-dotenv** – environment variables
- **requests** – API calls
- **python-multipart** – file uploads

---

## 📁 Project Structure

    rag-chat-backend/
    │
    ├── app/
    │ ├── main.py # FastAPI app & routes
    │ └── rag/
    │ ├── pdf_loader.py
    │ ├── chunker.py
    │ ├── embeddings.py
    │ ├── vector_store.py
    │ └── qa.py
    │
    ├── data/
    │ ├── uploads/ # Uploaded PDFs (ignored by git)
    │ └── chroma/ # Vector DB data (ignored by git)
    │
    ├── .env # API keys (not committed)
    ├── .gitignore
    ├── requirements.txt
    └── README.md


> ⚠️ The `data/` directory is **intentionally ignored** and regenerated at runtime.

---

## 🔐 Environment Variables

Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here

---

## ▶️ Running Locally

### 1️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start the server

```bash
uvicorn app.main:app --reload
```
Server will be available at: ```http://127.0.0.1:8000```
Swagger UI: ```http://127.0.0.1:8000/docs```


## 🧪 How to Test

1. Open the **Swagger UI** in your browser

2. Use `POST /upload` to upload a **text-based PDF file**.

3. After a successful upload, use `POST /ask` to ask questions related to the uploaded document.

If the system is working correctly, the answers returned should be grounded in the content of the uploaded PDF.

---

## ⚠️ Limitations (Intentional)

- No authentication
- Single shared vector store
- Local storage only
- Embeddings are regenerated if local data is deleted
- Not optimized for production use

These limitations are intentional to keep the project focused on **learning the core RAG workflow**.

---

## 🚀 Planned Enhancements

- User authentication using JWT
- Multi-chat support with isolated histories
- Per-chat and global document scoping
- Registration limits for controlled access
- Automatic cleanup of old PDFs
- Deployment on free hosting platforms (e.g., Render)

---

## 📌 Purpose

This project is built to:
- understand how **Retrieval-Augmented Generation (RAG)** works internally
- learn backend system design for AI-powered applications
- experiment with **LLMs and vector databases**
- serve as a **learning and portfolio project**

---

