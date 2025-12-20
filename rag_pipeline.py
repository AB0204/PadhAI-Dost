from langchain_community.vectorstores import FAISS
try:
    from langchain.chains import RetrievalQA
except ImportError:
    try:
        from langchain.chains.retrieval_qa.base import RetrievalQA
    except ImportError:
        try:
            from langchain_community.chains import RetrievalQA
        except ImportError:
            try:
                from langchain_classic.chains import RetrievalQA
            except ImportError:
                 raise ImportError("Could not import RetrievalQA from any known path.")
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_rag_pipeline(text, api_key):
    # Use Google's API-based embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)

    # Create a FAISS vectorstore (In-memory, fast, no SQLite dependency)
    # db = FAISS.from_texts(texts, embeddings_model) <--- OLD, prone to 429 errors

    # Robust Implementation: Batching + Retries
    import time
    import random
    
    db = None
    batch_size = 5 # Process 5 chunks at a time to stay under rate limits
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        retry_count = 0
        max_retries = 5
        
        while retry_count < max_retries:
            try:
                if db is None:
                    db = FAISS.from_texts(batch, embeddings_model)
                else:
                    new_db = FAISS.from_texts(batch, embeddings_model)
                    db.merge_from(new_db)
                break # Success, move to next batch
            except Exception as e:
                # Check for rate limit error (usually 429)
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    retry_count += 1
                    wait_time = (2 ** retry_count) + random.uniform(0, 1) # Exponential backoff
                    print(f"Rate limit hit. Retrying batch {i//batch_size} in {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    raise e # Re-raise other errors
        
        if retry_count == max_retries:
            raise RuntimeError("Failed to process document due to persistent rate limiting. Please try a smaller file.")
            
        # Optional: Pulse sleep between successful batches to be nice to the API
        time.sleep(1)
    
    # Save locally if needed, but for ephemeral Streamlit usage, in-memory is fine.
    # db.save_local("faiss_index") 
    
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=db.as_retriever())
    return qa