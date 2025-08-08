import os
from llama_cpp import Llama
from dotenv import load_dotenv

load_dotenv()

# Path to your local Llama model (download a GGUF file, e.g., llama-2-7b.Q4_K_M.gguf)
LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "llama-2-7b.Q4_K_M.gguf")
llm = Llama(model_path=LLAMA_MODEL_PATH, n_ctx=2048)

def answer_question(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:"""
    response = llm(
        prompt,
        max_tokens=500,
        temperature=0.2,
        stop=["\n"]
    )
    return response["choices"][0]["text"].strip()

def get_answers(query: str, vector_store):
    """
    Takes a query and a vector store, retrieves relevant chunks, and returns LLM answer
    """
    try:
        # Perform similarity search to get relevant chunks
        results = vector_store.similarity_search(query, k=3)
        context_chunks = [doc.page_content for doc in results]
        
        # Use LLM to generate answer based on context
        answer = answer_question(query, context_chunks)
        return answer
    except Exception as e:
        raise RuntimeError(f"Error getting answers: {str(e)}")

def process_document(file_path: str, questions: list[str]):
    """
    Process a document and answer questions about it
    """
    try:
        from services.vector_store import process_document as process_doc
        vector_store = process_doc(file_path)
        
        answers = []
        for question in questions:
            answer = get_answers(question, vector_store)
            answers.append({"question": question, "answer": answer})
        
        return answers
    except Exception as e:
        raise RuntimeError(f"Error processing document: {str(e)}")
