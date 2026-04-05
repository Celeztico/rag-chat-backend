def chunk_text(text: str, chunk_size=500, overlap=100):
    # return if small text
    if len(text) <= 800:
        return [text]

    # else chunking with overlap
    chunks = []
    start = 0 

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks