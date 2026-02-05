# 📄 RAG Backend – PDF-based Question Answering

This is a **backend-only learning project** that implements a **Retrieval-Augmented Generation (RAG)** system.

This system supports secure **authentication**, **multi-chat conversations**,
**global** and **chat-specific document storage**, and **isolated RAG pipelines per user**.

---

## ✨ Features (Current Phase)

### 🔐 Authentication
- User registration and login
- OAuth2 password flow
- JWT-based session management
- Secure Argon2 password hashing
- Registration limits and controls (for testing purposes)

### 💬 Chat System
- Multiple chats per user
- Chat-based conversation structure
- User-level isolation

### 📄 Document Management
- Upload text-based PDF files
- Global document support
- Chat-specific document support
- Organized per-user storage
- Automatic ingestion into vector database

### 🧠 RAG Pipeline
- PDF text extraction
- Text chunking
- Embedding generation
- Vector storage using ChromaDB
- Metadata-based filtering
- Scoped retrieval (user + chat + global)

### 🤖 LLM Integration
- Groq API
- Context-grounded responses
- Reduced hallucination behavior

---

## 🧠 Tech Stack

### Backend
- **Python 3**
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI server

### Database
- **SQLite** (development)
- **SQLAlchemy ORM**

### Authentication
- **OAuth2PasswordBearer**
- **JWT (python-jose)**
- **Argon2 (passlib)**

### RAG Pipeline
- **PyPDF** – PDF text extraction
- **Sentence-Transformers** – local embeddings (`all-MiniLM-L6-v2`)
- **ChromaDB (local)** – vector database
- **Groq API** – LLM for answering questions

### Utilities
- **python-dotenv** – environment variables
- **requests** – API calls
- **python-multipart** – file uploads
- **pydantic[email]** – email-validator

---

## 📁 Project Structure

    rag-chat-backend/
    │
    ├── app/
    │ ├── auth/ # Authentication
    │ ├── chats/ # Chat management
    │ ├── db/ # Database config
    │ ├── documents/ # PDF storage
    │ ├── rag/ # RAG pipeline
    │ └── main.py # App entry point
    │
    ├── data/
    │ ├── uploads/ # Uploaded PDFs (ignored by git)
    │ └── chroma/ # Vector DB data (ignored by git)
    │
    ├── .env # API keys (not committed)
    ├── .gitignore
    ├── requirements.txt
    └── README.md


> ⚠️ The `data/` directory is **intentionally ignored** and need to be regenerated at runtime.

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```ini
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_jwt_secret # for now its hardcoded but is best practice use env
```

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

---

## 🧪 API Usage Flow

Follow the steps below to use the system end-to-end.

---

### 1️⃣ Register User

Create a new user account.

```bash
POST /auth/register
```

---

### 2️⃣ Login

Authenticate and receive a JWT token.

```bash
POST /auth/login
```

The response contains:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

### 3️⃣ Create Chat

Create a new chat session.

```bash
POST /chats
```
Request Body:

for shared data
```json
{
  "title": "My Notes",
  "scope": "global"
}
```
OR

for chat specific data
```json
{
  "title": "OS Notes",
  "scope": "chat"
}
```

---

### 4️⃣ Upload PDF

Upload and ingest a PDF document.

```bash
POST /documents/upload/{chat_id}
```
- **chat_id** → ID of the target chat
- File → PDF document

The file is automatically processed and added to the vector database.

---

### 5️⃣ Ask a Question

Query the RAG system.

```bash
POST /ask
```

Request body:
```json
{
  "chat_id": 2,
  "question": "Explain virtual memory"
}
```

The system retrieves relevant context and generates an answer.

---

---

## 📂 Storage Layout

---

### File System Structure

Uploaded documents are organized as:

    data/
    └──uploads/
       └──user_id/
          ├──global/ # context shared between chats
          └──chat_2/ # each separate non shared chat with id

---

### Vector Metadata Format

Each indexed chunk contains:

```ini
user_id = "1"
chat_id = "global" | "2"
```
This enables strict per-user and per-chat filtering.

---

## 🔒 Security Model

The system enforces security at multiple layers:

- Argon2 password hashing
- JWT-based authentication
- OAuth2-compliant login flow
- Per-user authorization checks
- Chat ownership validation
- Scoped vector retrieval
- No cross-user data leakage

---

## ⚠️ Current Limitations

The following features are intentionally not implemented yet:

- Persistent message history
- Source citation display
- Frontend user interface
- Streaming responses
- Production-grade database

These will be addressed in later phases.

---

## 🚀 Planned Enhancements

- Chat message persistence
- Source attribution and citations
- Automatic cleanup of old data/PDFs
- Usage quotas and rate limiting
- Admin management dashboard
- Deployment hardening
- Web frontend application

---

## 📌 Purpose

This project is built to:
- Understand how **Retrieval-Augmented Generation (RAG)** works internally
- Learn **modern backend** architecture
- experiment with **LLMs and vector databases**
- Practice **secure authentication systems**
- Implement **production-style RAG pipelines**
- Understand **multi-tenant data isolation**
- serve as a **learning and portfolio project**

---

## ⚠️ **Disclaimer**

This project is intended for learning and experimental use only.

It should not be deployed to production environments without
additional security reviews, performance testing, and monitoring.

---

