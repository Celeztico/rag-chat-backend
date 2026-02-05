from pydantic import BaseModel

class DocumentOut(BaseModel):
    id: int
    filename: str
