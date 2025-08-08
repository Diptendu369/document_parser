import sqlite3
from datetime import datetime
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
DB_NAME = "documents.db"
embedding_model = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
DB_DIR = "faiss_index"

def load_db():
    return FAISS.load_local(DB_DIR, embedding_model)

def save_db(db):
    db.save_local(DB_DIR)
def init_db():
    print("Database initialized!")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_document(filename: str, text: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO documents (filename, text, timestamp) VALUES (?, ?, ?)", 
              (filename, text, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
