from pypdf import PdfReader

def extract_text(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        p_txt = page.extract_text()
        if p_txt:
            text.append(p_txt)
    return "\n".join(text)