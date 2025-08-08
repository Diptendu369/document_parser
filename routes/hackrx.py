# routes/hackrx.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vector_store import process_document  # assumes this function parses and embeds
from services.llm_service import get_answers        # assumes this answers based on vector search
import requests
import os

router = APIRouter()

class HackRxRequest(BaseModel):
    document_url: str
    questions: list[str]

@router.post("/hackrx/run")
async def run_hackrx_query(request: HackRxRequest):
    try:
        # Step 1: Download the document
        response = requests.get(request.document_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download document")

        filename = request.document_url.split("/")[-1]
        file_path = os.path.join("data", filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

        # Step 2: Process the document
        vector_store = process_document(file_path)

        # Step 3: Get answers
        answers = []
        for q in request.questions:
            answer = get_answers(q, vector_store)
            answers.append({"question": q, "answer": answer})

        return {"status": "success", "answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
