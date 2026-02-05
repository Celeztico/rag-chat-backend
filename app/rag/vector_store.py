import chromadb

client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="data/chroma"
    )
)

collection = client.get_or_create_collection("rag_test")

def debug_count():
    return collection.count()


def add_documents(chunks, embeddings, user_id, chat_id):
    ids = [f"{user_id}_{chat_id}_{i}" for i in range(len(chunks))]
    chat_value = "global" if chat_id is None else str(chat_id)

    metadata = [
        {"user_id": user_id, "chat_id": chat_value}
        for _ in chunks
    ]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids
    )

def search(query_embedding,user_id, chat_id, k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where={
            "$and": [
                {"user_id": user_id},
                {
                    "$or": [
                        {"chat_id": "global"},
                        {"chat_id": str(chat_id)}
                    ]
                }
            ]
        }
    )
