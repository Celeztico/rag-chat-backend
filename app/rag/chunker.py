def chunk_text(text: str, size=500, overlap=100):
    chunks = []
    start = 0 

    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks