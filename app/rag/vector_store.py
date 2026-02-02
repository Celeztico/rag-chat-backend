import chromadb

client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="data/chroma"
    )
)

collection = client.get_or_create_collection("rag_test")

def add_documents(chunks, embeddings):
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

def search(query_embedding, k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
