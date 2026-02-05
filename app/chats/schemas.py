from pydantic import BaseModel

class ChatCreate(BaseModel):
    title: str
    scope: str  # "global" or "chat"

class AskRequest(BaseModel):
    chat_id: int
    question: str