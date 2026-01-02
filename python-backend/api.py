from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from document_loader import load_document
from rag_pipeline import create_rag_pipeline
from pucho import pucho
from samjha_do import samjha_do
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Global store for RAG pipelines (in-memory for simple dev, use DB/VectorStore in prod)
# { "session_id": rag_chain }
rag_store = {}
texts_store = {} # Store raw text for Pucho/SamjhaDo

class ChatRequest(BaseModel):
    session_id: str
    message: str

class PuchoRequest(BaseModel):
    session_id: str
    num_questions: int = 5
    difficulty: int = 5
    type: str = "Subjective"

class ExplainRequest(BaseModel):
    session_id: str
    level: str = "Intermediate"

@app.post("/upload")
async def upload_document(session_id: str, file: UploadFile = File(...)):
    try:
        # Save temp file
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load and Process
        text = load_document(temp_filename) # Adjusted to accept path or file object depending on implementation
        # Our load_document usually takes a file-like object or path. Let's check implementation. 
        # Assuming path for safety.
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Gemini API Key missing")
            
        rag_chain = create_rag_pipeline(text, api_key)
        
        # Store in memory
        rag_store[session_id] = rag_chain
        texts_store[session_id] = text
        
        # Cleanup
        os.remove(temp_filename)
        
        return {"status": "success", "message": "Document processed and RAG ready"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    if session_id not in rag_store:
        return {"answer": "Please upload a document first."}
    
    rag = rag_store[session_id]
    response = rag.run(request.message) # Adjust based on LangChain chain .run or .invoke
    return {"answer": response}

@app.post("/pucho")
async def generate_questions(request: PuchoRequest):
    session_id = request.session_id
    if session_id not in texts_store:
        raise HTTPException(status_code=400, detail="No document uploaded")
        
    text = texts_store[session_id]
    api_key = os.getenv("GEMINI_API_KEY")
    questions = pucho(text, request.type, request.num_questions, request.difficulty, api_key)
    return {"questions": questions}

@app.post("/explain")
async def explain_concept(request: ExplainRequest):
    session_id = request.session_id
    if session_id not in texts_store:
        raise HTTPException(status_code=400, detail="No document uploaded")
        
    text = texts_store[session_id]
    api_key = os.getenv("GEMINI_API_KEY")
    explanation = samjha_do(text, request.level, api_key)
    return {"explanation": explanation}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
