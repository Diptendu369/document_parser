from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from pathlib import Path
from constants import FAISS_INDEX_PATH
import os
import shutil

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_and_store(pdf_path: str, index_dir: str = "output/faiss_index"):
    try:
        # 1. Load and split PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = splitter.split_documents(pages)

        # 2. Load local embedding model
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 3. Ensure output directory exists
        os.makedirs(index_dir, exist_ok=True)
        index_path = Path(index_dir) / "index.faiss"

        if index_path.exists():
            # Load existing index and merge with new documents
            db = FAISS.load_local(index_dir, embeddings=embedding_model ,allow_dangerous_deserialization=True)
            new_db = FAISS.from_documents(documents, embedding_model)
            db.merge_from(new_db)
        else:
            # Create new FAISS index
            db = FAISS.from_documents(documents, embedding_model)

        # 4. Save index to disk
        db.save_local(index_dir)
        print("Indexing completed successfully.")

    except Exception as e:
        raise RuntimeError(f"Error during embedding and storing: {str(e)}")


def query_index(query: str, index_dir: str = "output/faiss_index", k: int = 3):
    try:
        # 1. Load same embedding model
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 2. Check if index exists
        if not Path(index_dir).joinpath("index.faiss").exists():
            raise FileNotFoundError(f"Index not found at: {index_dir}/index.faiss")

        # 3. Load FAISS index
        db = FAISS.load_local(index_dir, embeddings=embedding_model, allow_dangerous_deserialization=True)


        # 4. Perform similarity search
        results = db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    except Exception as e:
        raise RuntimeError(f"Error during similarity search: {str(e)}")

def save_vector_store(docs: list[Document]):
    if os.path.exists(FAISS_INDEX_PATH):
        # Try loading existing FAISS index
        try:
            vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
            vectorstore.add_documents(docs)
        except Exception as e:
            print(f"FAISS load failed: {e} — recreating index")
            shutil.rmtree(FAISS_INDEX_PATH, ignore_errors=True)
            vectorstore = FAISS.from_documents(docs, embedding_model)
    else:
        vectorstore = FAISS.from_documents(docs, embedding_model)

    vectorstore.save_local(FAISS_INDEX_PATH)

def load_vector_store():
    return FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)

def process_document(file_path: str):
    """
    Takes file_path of PDF/DOCX/email and returns the vector store (FAISS or equivalent)
    """
    try:
        # Load and split PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = splitter.split_documents(pages)

        # Create FAISS index
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(documents, embedding_model)
        
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Error processing document: {str(e)}")
