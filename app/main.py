import shutil
from fastapi import UploadFile, File, FastAPI, Depends, HTTPException
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

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG Learning Project")

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
    
    # Save user message
    msg = Message(
        chat_id=data.chat_id,
        role="user",
        content=data.question
    )
    db.add(msg)
    db.commit()

    messages = db.query(Message).filter(
        Message.chat_id == data.chat_id
    ).order_by(Message.created_at.desc()).limit(6).all()

    messages.reverse()

    history = "\n".join(
    f"{m.role}: {m.content}" for m in messages
    )
        
    answer,docs = answer_question(data.question, user.id, data.chat_id, history)

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
        "sources": docs
    }

from app.rag.vector_store import debug_count

@app.get("/debug/chroma")
def debug_chroma():
    return {"count": debug_count()}