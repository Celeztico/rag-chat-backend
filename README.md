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
- Persistent message history per chat
- Context-aware conversations using chat history

### 📄 Document Management
- Upload text-based PDF files
- Global document support
- Chat-specific document support
- Organized per-user storage
- Automatic ingestion into vector database
- Background processing for PDF ingestion
- Document processing status tracking (processing, ready, failed)

### 🧠 RAG Pipeline
- PDF text extraction
- Adaptive Text chunking (small docs → single chunk, large docs → overlapping chunks)
- Embedding generation
- Vector storage using ChromaDB
- Metadata-based filtering
- Scoped retrieval (user + chat + global)
- Relevance filtering with fallback mechanism
- Structured citations with metadata (filename, chunk index)
- No-context fallback handling to prevent hallucinated answers

### ⚡ Async Processing
- BackgroundTasks-based PDF ingestion
- Non-blocking upload endpoint
- Status-based query gating (prevents querying before indexing)

### 🤖 LLM Integration
- Groq API
- Context-grounded responses
- Context-enforced answering (no answer without retrieved context)
- Citation-aware responses referencing source chunks

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
- **ChromaDB (local)** – persistent vector database
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

The file is uploaded immediately and processed asynchronously in the background.

Use the status endpoint to check when processing is complete before querying.

---

### 5️⃣ Check Processing Status

Check whether uploaded documents are ready for querying.

```bash
GET /documents/status/{chat_id}
```

Response:

```json
{
  "status": "processing" | "ready" | "failed" | "no_documents"
}
```

---

### 6️⃣ Ask a Question

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


Returns a context-aware response with citations.

If documents are still processing, returns:

```http
HTTP/1.1 202 Accepted
```

---

## 📂 Storage Layout


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

## 🧹 Data Management

- Automatic cleanup of old uploaded files on server startup
- Configurable retention period for uploaded documents

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
- Query blocked until document processing is complete
- No response generated without verified context

---

## ⚠️ Current Limitations

The following features are intentionally not implemented yet:

- Frontend user interface
- Streaming responses
- Production-grade database
- SQLite used for development (not production-ready)
- Background processing is not fault-tolerant (no job queue yet)

These will be addressed in later phases.

---

## 🚀 Planned Enhancements

- Streaming responses
- Usage quotas and rate limiting
- Admin management dashboard
- Deployment hardening
- Web frontend application
- Production database integration (PostgreSQL / Supabase)
- Distributed task queue (Celery / workers)

---

## ⚙️ System Behavior

- PDF uploads are processed asynchronously
- Queries are only allowed after document indexing is complete
- Retrieval uses:
  - User isolation
  - Chat-based scoping
  - Global + chat document merging
- If no relevant context is found, the system returns a fallback response instead of generating an answer

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

