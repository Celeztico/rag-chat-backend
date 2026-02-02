import shutil
from fastapi import UploadFile, File, FastAPI
from app.rag.pdf_loader import extract_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_documents
from app.rag.qa import answer_question

app = FastAPI(title="RAG Learning Project")

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
def ask(question: str):
    answer = answer_question(question)
    return {"answer": answer}