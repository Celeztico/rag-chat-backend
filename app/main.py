import shutil
import asyncio
from fastapi import UploadFile, File, FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from app.rag.pdf_loader import extract_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_documents
from app.rag.qa import answer_question
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.db.database import engine, Base
from app.auth.models import User
from app.auth.routes import router as auth_router
from app.auth.security import get_current_user
from app.chats.models import Chat, Message
from app.documents.models import Document
from app.chats.routes import router as chat_router
from app.documents.routes import router as doc_router
from app.chats.schemas import AskRequest
from app.utils.cleanup import cleanup_uploads

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # 🔹 Startup logic
    print("Running cleanup on startup...")
    await asyncio.to_thread(cleanup_uploads, days=7)

    yield

    # 🔹 Shutdown logic (temporary logic )
    print("Shutting down app...")


app = FastAPI(title="RAG Learning Project", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(doc_router)

@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    path = f"data/uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(path)
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    add_documents(chunks, embeddings)

    return {"chunks_added": len(chunks)}

@app.post("/ask")
def ask(
    data: AskRequest, 
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
    ):

    chat = db.query(Chat).filter(
        Chat.id == data.chat_id,
        Chat.user_id == user.id
    ).first()

    if not chat:
        raise HTTPException(404, "Chat not found")
    
    docs = db.query(Document).filter(
    Document.chat_id == data.chat_id,
    Document.user_id == user.id
    ).all()

    if any(doc.status != "ready" for doc in docs):
        raise HTTPException(202, "Documents are still being processed. Try again shortly.")
    
    # Save user message
    msg = Message(
        chat_id=data.chat_id,
        role="user",
        content=data.question
    )
    db.add(msg)
    db.commit()

    # NOTE: build hybrid history with semantic search in future after most of the important things are done for now use heuristic history.
    messages = db.query(Message).filter(
        Message.chat_id == data.chat_id
    ).order_by(Message.created_at.desc()).limit(6).all()

    messages.reverse()

    history = "\n".join(
        f"{m.role.upper()}: {m.content}" 
        for m in messages
    )
    history = history[-2000:]  # trim history if too long
    answer,sources = answer_question(data.question, user.id, data.chat_id, history)

    # Save assistant message
    msg = Message(
        chat_id=data.chat_id,
        role="assistant",
        content=answer
    )
    db.add(msg)
    db.commit()

    return {
        "answer": answer,
        "sources": sources
    }

from app.rag.vector_store import debug_count

@app.get("/debug/chroma")
def debug_chroma():
    return {"count": debug_count()}