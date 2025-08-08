# routes/query_pdf.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.vector_store import query_index


router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: list

@router.post("/query-pdf/", response_model=QueryResponse)
async def query_pdf(data: QueryRequest):
    try:
        results = query_index(data.query)

        return {"results": results}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
