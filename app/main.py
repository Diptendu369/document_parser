from fastapi import FastAPI
from dotenv import load_dotenv
from routes.upload_pdf import router as upload_router
from routes.query_pdf import router as query_router
from routes.hackrx import router as hackrx_router
import os

# Load environment variables from .env (if needed)
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="LLM-Powered Query-Retrieval System",
    description="Query your PDFs using local embeddings + FAISS",
    version="1.0.0"
)

# Include Routers
app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(hackrx_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "LLM Query System is running using free, local models"}
