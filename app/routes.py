from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from services.vector_store import embed_and_store
from pydantic import BaseModel
from fastapi import APIRouter
from routes.upload_pdf import router as upload_pdf_router
from services.vector_store import process_document

router = APIRouter()

class DocumentRequest(BaseModel):
    url: str
    questions: list[str]

@router.post("/hackrx/run")
async def hackrx_run(request: DocumentRequest):
    return {"message": "Received", "url": request.url, "questions": request.questions}
# Include the upload_pdf route
router.include_router(upload_pdf_router, prefix="/api")
router.include_router(hackrx.router) 
@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = Path("data") / file.filename
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Call the vector store logic and specify output dir
        embed_and_store(str(file_path), index_dir="output/faiss_index")

        return {"message": "PDF uploaded and processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
