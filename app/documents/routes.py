import os, shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.chats.models import Chat
from app.db.database import get_db
from app.auth.security import get_current_user
from app.documents.models import Document
from app.rag.ingest import process_pdf_for_rag

UPLOAD_ROOT = "data/uploads"

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload/{chat_id}")
def upload_document(
    chat_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Get chat
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == user.id
    ).first()

    if not chat:
        raise HTTPException(404, "Chat not found")

    # Decide folder based on scope
    if chat.scope == "global":
        folder = f"{UPLOAD_ROOT}/{user.id}/global"
        chroma_chat_id = None   # will become "global"
    else:
        folder = f"{UPLOAD_ROOT}/{user.id}/chat_{chat_id}"
        chroma_chat_id = chat_id

    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{file.filename}"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc = Document(
        user_id=user.id,
        chat_id=chat_id,
        filename=file.filename,
        path=path
    )

    db.add(doc)
    db.commit()

      # Process for RAG
    process_pdf_for_rag(
        path,
        user.id,
        chroma_chat_id
    )

    return {"message": "Uploaded"}
