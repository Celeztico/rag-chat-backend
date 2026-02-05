from app.rag.pdf_loader import extract_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_documents

# remove log statements in future

def process_pdf_for_rag(path, user_id, chat_id):

    # print("INGESTING:", path, user_id, chat_id)

    text = extract_text(path)

    # print("TEXT LENGTH:", len(text))

    if not text.strip():
        # print("EMPTY TEXT, SKIPPING")
        return

    chunks = chunk_text(text)
    # print("CHUNKS:", len(chunks))

    embeddings = embed_texts(chunks)
    # print("EMBEDDINGS:", len(embeddings))

    add_documents(
        chunks,
        embeddings,
        user_id,
        chat_id
    )
    # print("ADDED TO CHROMA")
