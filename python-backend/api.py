from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from document_loader import load_document
from rag_pipeline import create_rag_pipeline
from pucho import pucho
from samjha_do import samjha_do
from dotenv import load_dotenv

# --- CONFIGURATION ---
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
DEMO_MODE = False

if not api_key:
    print("⚠️  WARNING: No API Key found. running in DEMO MODE.")
    DEMO_MODE = True
else:
    print("✅ API Key found. AI features enabled.")

app = FastAPI()

# Enable CORS for Vercel Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global store
rag_store = {}
texts_store = {}

# ... Models ...
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

@app.get("/")
def health_check():
    status = "Demo Mode 🟡" if DEMO_MODE else "Online 🟢"
    return {"status": "ok", "message": f"PadhAI Dost Backend is Running ({status})"}

@app.post("/upload")
async def upload_document(session_id: str, file: UploadFile = File(...)):
    try:
        # Save temp file
        temp_filename = f"temp_{session_id}_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load Text
        text = load_document(temp_filename)
        
        # Store for non-RAG features
        texts_store[session_id] = text

        if not DEMO_MODE:
            # REAL MODE: Create Envelope
            rag_chain = create_rag_pipeline(text, api_key)
            rag_store[session_id] = rag_chain
        else:
            # DEMO MODE: Mock Store
            # We don't create embeddings to save time/errors
            rag_store[session_id] = "mock_rag_pipeline"

        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        msg = "Document processed (Demo)." if DEMO_MODE else "Document processed and RAG ready."
        return {"status": "success", "message": msg}
        
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id
    
    if DEMO_MODE:
        import random
        demo_responses = [
            "This is a demo response. In the live version, I would analyze your document.",
            "Interesting question! Connect an API Key to get a real AI answer based on the PDF.",
            "I see you're asking about the document. This is a static demo placeholder.",
        ]
        return {"answer": f"🤖 [DEMO]: {random.choice(demo_responses)}"}

    if session_id not in rag_store:
        return {"answer": "Please upload a document first."}
    
    rag = rag_store[session_id]
    try:
        response = rag.run(request.message) 
        return {"answer": response}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

@app.post("/pucho")
async def generate_questions(request: PuchoRequest):
    if DEMO_MODE:
        return {"questions": [
            "1. [DEMO] What is the main topic of this document?",
            "2. [DEMO] Explain the key concept on page 1.",
            "3. [DEMO] Who is the author of this file?",
            "4. [DEMO] What are the limitations mentioned?",
            "5. [DEMO] summarize the conclusion."
        ]}
        
    session_id = request.session_id
    if session_id not in texts_store:
        raise HTTPException(status_code=400, detail="No document upload found.")
        
    text = texts_store[session_id]
    questions = pucho(text, request.type, request.num_questions, request.difficulty, api_key)
    return {"questions": questions}

@app.post("/explain")
async def explain_concept(request: ExplainRequest):
    if DEMO_MODE:
        return {"explanation": "🎓 [DEMO EXPLANATION]: This concept is very interesting! In a real deployment, I would use the LLM to simplify this based on your document's context."}

    session_id = request.session_id
    if session_id not in texts_store:
        raise HTTPException(status_code=400, detail="No document upload found.")
        
    text = texts_store[session_id]
    explanation = samjha_do(text, request.level, api_key)
    return {"explanation": explanation}

@app.post("/generate-flashcards")
async def generate_flashcards(request: ChatRequest):
    # This was already a stub, but let's make it consistent
    mock_cards = [
        {"front": "What is PadhAI Dost?", "back": "An AI-powered study companion."},
        {"front": "Is this Real AI?", "back": "Currently running in Demo Mode (No API Key)."},
        {"front": "Feature", "back": "Auto-Flashcards generate Q&A from PDFs."}
    ]
    
    # In real mode we might want real generation, but for now the stub applies to both 
    # or we can differentiate if we implemented real logic.
    return {"flashcards": mock_cards}



if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable for deployment (Railway/Render)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
