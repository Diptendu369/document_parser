from fastapi import APIRouter, UploadFile, File, HTTPException
from services.vector_store import embed_and_store
import os
from services.llm_service import process_document
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class RunRequest(BaseModel):
    url: str
    questions: list[str]

@router.post("/api/v1/hackrx/run")
async def run_query(request: RunRequest):
    try:
        answers = process_document(request.url, request.questions)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/hackrx/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded PDF
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Embed and store the document
        embed_and_store(file_path)

        return {
            "message": "PDF uploaded and processed successfully",
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
