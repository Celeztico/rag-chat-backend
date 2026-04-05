import os
import requests
from dotenv import load_dotenv
from .embeddings import embed_texts
from .vector_store import search

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API=os.getenv('GROQ_API_KEY')
# print("GROQ_API Key:", GROQ_API)

def ask_groq(prompt: str) -> str:
    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def answer_question(question, user_id, chat_id, history):
    query_embedding = embed_texts([question])[0]
    results = search(query_embedding, user_id, chat_id)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    sources = [
        {
            "text": doc,
            "file": meta["filename"],
            "chunk": meta["chunk_index"]
        }
        for doc, meta in zip(docs, metas)
    ]
    context = ""
    for i, doc in enumerate(docs):
        context += f"[{i}] {doc}\n"

    prompt = f"""
Answer the question using ONLY the context below.

Each chunk has a number [i]. If you use information from a chunk, cite it like this: [i]([0], [1], ...).
Context:
{context}

Conversation so far:
{history}

Question:
{question}

Answer:
"""
    answer = ask_groq(prompt)
    return answer, sources
