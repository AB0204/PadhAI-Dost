from langchain_community.vectorstores import FAISS
try:
    from langchain.chains import RetrievalQA
except ImportError:
    from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_rag_pipeline(text, api_key):
    # Use Google's API-based embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)

    # Create a FAISS vectorstore (In-memory, fast, no SQLite dependency)
    db = FAISS.from_texts(texts, embeddings_model)
    
    # Save locally if needed, but for ephemeral Streamlit usage, in-memory is fine.
    # db.save_local("faiss_index") 
    
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=db.as_retriever())
    return qa