import os
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO

def parse_document(filename, content_bytes):
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return parse_pdf(content_bytes)
    elif ext == ".docx":
        return parse_docx(content_bytes)
    else:
        raise ValueError("Unsupported file format")

def parse_pdf(content_bytes):
    text = ""
    with fitz.open(stream=content_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.split("\n\n")

def parse_docx(content_bytes):
    doc = Document(BytesIO(content_bytes))
    text = "\n".join([p.text for p in doc.paragraphs])
    return text.split("\n\n")
