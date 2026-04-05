from app.rag.pdf_loader import extract_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_documents
from app.documents.models import Document
from app.utils.logger import logger

def process_pdf_for_rag(path, user_id, chat_id, doc_id, db):

    try:
        text = extract_text(path)

        if not text.strip():
            return

        chunks = chunk_text(text)

        embeddings = embed_texts(chunks)

        add_documents(
            chunks,
            embeddings,
            user_id,
            chat_id,
            filename=path.split("/")[-1]
        )

        doc = db.query(Document).get(doc_id)
        doc.status = "ready"
        db.commit()

        logger.info(f"INGESTING: {path},{user_id},{chat_id} - Chunks: {len(chunks)}, Embeddings: {len(embeddings)} Document ID: {doc_id} status: ready")
    except Exception as e:
        doc = db.query(Document).get(doc_id)
        doc.status = "failed"
        db.commit()

        logger.error(f"Error processing PDF for RAG: {e}")
        logger.info(f"INGESTING: {path},{user_id},{chat_id} - Document ID: {doc_id} status: failed")

