from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.security import get_current_user
from app.chats.models import Chat
from app.chats.schemas import ChatCreate

router = APIRouter(prefix="/chats", tags=["chats"])
@router.post("/")
def create_chat(
    data: ChatCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chat = Chat(
        user_id=user.id,
        title=data.title,
        scope=data.scope
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat

@router.get("/")
def list_chats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Chat).filter(Chat.user_id == user.id).all()
