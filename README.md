## Document Parser
This project allows you to upload PDF documents, convert their contents into vector embeddings using HuggingFace Sentence Transformers, store them in a FAISS vector database, and perform semantic search on the stored content.

It is built with FastAPI for serving APIs, LangChain for embedding & document handling, and FAISS for efficient similarity search.
Ngrok is used to expose local APIs to the internet for webhook integrations.

## 🛠️ Features ###
PDF Upload API (/api/upload-pdf/) – Uploads and processes a PDF, splitting it into chunks and storing embeddings in FAISS.

Semantic Search API – Query stored PDFs and retrieve the most relevant text chunks.

Local or Remote Access – Run locally or expose via ngrok for public access.

Persistent Storage – Saves FAISS index locally for reuse.

HuggingFace Embeddings – Uses the all-MiniLM-L6-v2 model for lightweight, high-quality embeddings.

## ⚙️ How It Works
###  Upload a PDF

You send a multipart/form-data POST request to /api/upload-pdf/ with a PDF file.

The PDF is loaded and split into text chunks using RecursiveCharacterTextSplitter.

Each chunk is embedded using HuggingFace's all-MiniLM-L6-v2 model.

Embeddings are stored in a local FAISS index.

### Query the PDF

A query string is embedded and compared against stored vectors.

FAISS returns the most similar chunks.

The relevant chunks are sent back in the API response.

### 📦 Installation
1️⃣ Clone the repository
```
git clone https://github.com/yourusername/pdf-qa-fastapi.git
cd pdf-qa-fastapi
```
2️⃣ Create a virtual environment
```
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
▶️ Running the Server
Start FastAPI:
```
uvicorn main:app --reload
```
This will run the server on:
```
http://127.0.0.1:8000
```
🌍 Expose to Internet via ngrok
```
ngrok http 8000
```
📡 API Endpoints
1. Upload PDF
POST /api/upload-pdf/

Request:

Content-Type: multipart/form-data

Field name: file

Example using curl:
```
curl -X POST "https://<your-ngrok-id>.ngrok-free.app/api/upload-pdf/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf;type=application/pdf"
```
Response:
```
json
Copy
Edit
{
  "message": "PDF uploaded and indexed successfully."
}
```
### Query Stored PDFs
POST /api/query/

Request:

```
{
  "query": "What is the policy number?"
}
```
Response:
```
{
  "results": [
    "Policy Number: 123456789",
    "This policy covers..."
  ]
}
```
