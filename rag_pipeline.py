from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_rag_pipeline(text, api_key):
    # Use Google's API-based embeddings (Fast, Light, No-Torch required)
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)

    # Create a Chroma vectorstore
    db = Chroma.from_texts(texts, embeddings_model, persist_directory="./chroma_db")
    
    # Simple persistence check (Chroma automatically persists on write in newer versions, 
    # but explicit call or client management is sometimes needed depending on version. 
    # For Streamlit ephemeral instances, this is fine).
    
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=db.as_retriever())
    return qa