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

def answer_question(question, user_id, chat_id):
    query_embedding = embed_texts([question])[0]
    results = search(query_embedding, user_id, chat_id)

    context_chunks = results["documents"][0]
    context = "\n".join(context_chunks)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""
    return ask_groq(prompt)
