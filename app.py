import streamlit as st
from document_loader import load_document
from rag_pipeline import create_rag_pipeline
from samjha_do import samjha_do
from pucho import pucho
from dotenv import load_dotenv
import os
import shutil
from media_handler import upload_media
from knowledge_graph import generate_knowledge_graph
import google.generativeai as genai

# Load API key from environment
# Load API key from environment or secrets
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Fallback to Streamlit secrets if not found in env
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.warning("Please enter your Gemini API key.")
    st.stop()

# Clean up the key (remove quotes or whitespace if user pasted incorrectly)
api_key = api_key.strip().strip('"').strip("'")

# Configure genai explicitly here to validate the key immediately
genai.configure(api_key=api_key)

try:
    # Quick test to verify key works before user does anything
    first_model = next(iter(genai.list_models()))
except Exception as e:
    st.error(f"🚨 Critical Error: Your Google Gemini API Key is invalid or not working.\n\nError Details: {e}")
    st.info("Please go to 'Manage App' -> 'Settings' -> 'Secrets' and verify your key.")
    st.stop()

# Initialize chat history if not already in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- CUSTOM CSS (Minimal Light Theme) ---
st.markdown(
    """
    <style>
    :root {
        --primary-bg: #ffffff;        /* Main background */
        --secondary-bg: #f9f9f9;        /* Container background */
        --accent-color: #3b82f6;        /* Buttons and highlight */
        --text-color: #333333;          /* Main text color */
        --border-color: #dddddd;        /* Light border color */
        --user-bubble: #dcf8c6;         /* User chat bubble background (light green) */
        --assistant-bubble: #ffffff;    /* Assistant bubble background (white) */
    }

    /* Page layout */
    .stApp {
        background-color: var(--primary-bg) !important;
        color: var(--text-color) !important;
        padding-bottom: 60px; /* space at the bottom for the pinned chat input */
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-color);
    }

    /* Chat container */
    .chat-container {
        background-color: var(--secondary-bg);
        padding: 10px;
        border-radius: 5px;
        max-height: calc(100vh - 200px);
        overflow-y: auto;
        border: 1px solid var(--border-color);
    }

    .user-message {
        text-align: right;
        background-color: var(--user-bubble);
        padding: 8px;
        border-radius: 6px;
        margin: 5px 0;
        color: #000000;
        border: 1px solid var(--border-color);
    }

    .assistant-message {
        text-align: left;
        background-color: var(--assistant-bubble);
        padding: 8px;
        border-radius: 6px;
        margin: 5px 0;
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }

    /* Buttons and inputs */
    .stButton > button {
        background-color: var(--accent-color) !important;
        color: #ffffff !important;
        border: none;
        border-radius: 4px;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
    }
    .stTextInput>div>div>input {
        color: var(--text-color);
        background-color: #ffffff;
        border: 1px solid var(--border-color);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_chat_history():
    """Renders the chat history from session state."""
    chat_placeholder.empty()
    with chat_placeholder.container():
        st.subheader("Chat History")
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(
                    f"<div class='user-message'><strong>You:</strong> {chat['message']}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='assistant-message'><strong>Assistant:</strong> {chat['message']}</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)


# Minimal header at the top
st.header("PadhAI Dost - Your Study Buddy")

# "Clear this chat" button clears the session state chat history
if st.button("Clear this chat"):
    st.session_state.chat_history = []

# Button in sidebar to clear chat history
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

chat_placeholder = st.empty()
render_chat_history()

# Sidebar: Document upload and extra features
with st.sidebar:
    st.header("Controls")
    st.subheader("Document & Media")
    uploaded_file = st.file_uploader("Upload PDF, TXT, MP3, WAV, MP4", type=["pdf", "png", "txt", "mp3", "wav", "mp4"])
    
    if not uploaded_file:
        st.info("Upload a file to start.")
        st.stop()

    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    # Handle Media Files (Audio/Video)
    if file_ext in ["mp3", "wav", "mp4"]:
        st.info("Media file detected. Switching to Lecture Sync Mode.")
        
        # Save temp file for upload
        with open("temp_media." + file_ext, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            with st.spinner("Uploading media to Gemini... This may take a moment."):
                media_file = upload_media("temp_media." + file_ext, api_key=api_key)
                st.session_state['active_media_file'] = media_file
                st.success("Media Ready! Ask questions below.")
        except Exception as e:
            st.error(f"Media Upload Failed: {e}")
            st.stop()
            
    # Handle Text Documents
    else:
        try:
            text = load_document(uploaded_file)
            st.success("Document loaded successfully!")
            rag = create_rag_pipeline(text, api_key)
            st.session_state['rag_pipeline'] = rag
            st.session_state['current_text'] = text # Store for knowledge graph
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()

    st.markdown("---")
    st.subheader("Tools")
    
    # Knowledge Graph Feature
    if file_ext not in ["mp3", "wav", "mp4"]:
        if st.button("Generate Knowledge Graph"):
            with st.spinner("Drawing detailed concept map..."):
                dot_code = generate_knowledge_graph(st.session_state.get('current_text', ''), api_key)
                st.graphviz_chart(dot_code)

    st.markdown("---")
    st.subheader("Other Features")

    # Display Samjha Do and Pucho side-by-side
    col1, col2 = st.columns(2)

    # Samjha Do feature in col1
    with col1:
        st.markdown("### Samjha Do")
        with st.expander("Configure Samjha Do"):
            prior_knowledge = st.selectbox(
                "Select your prior knowledge:",
                ["Beginner", "Intermediate", "Advanced"],
                key="samjha_prior"
            )
            if st.button("Submit Samjha Do", key="samjha_submit"):
                st.session_state.chat_history.append({"role": "user", "message": "Samjha Do"})
                render_chat_history()
                with st.spinner("Explaining..."):
                    explanation = samjha_do(text, prior_knowledge, api_key)
                st.session_state.chat_history.append({"role": "assistant", "message": explanation})
                render_chat_history()

    # Pucho feature in col2
    with col2:
        st.markdown("### Pucho")
        with st.expander("Configure Pucho"):
            question_type = st.radio("Type of Questions:", ["Subjective", "Objective"], key="pucho_type")
            num_questions = st.number_input("Number of Questions (1-50):", min_value=1, max_value=50, value=10, key="pucho_num")
            difficulty = st.slider("Difficulty (1-10):", min_value=1, max_value=10, value=5, key="pucho_diff")
            if st.button("Submit Pucho", key="pucho_submit"):
                st.session_state.chat_history.append({"role": "user", "message": "Pucho"})
                render_chat_history()
                with st.spinner("Generating questions..."):
                    questions = pucho(text, question_type, num_questions, difficulty, api_key)
                questions_str = "\n".join(questions)
                st.session_state.chat_history.append({"role": "assistant", "message": questions_str})
                render_chat_history()

# Use Streamlit’s built-in st.chat_input for pinned chat input at the bottom of the page
# Chat Input Handling
user_question = st.chat_input("Ask a question about your material...")
if user_question:
    st.session_state.chat_history.append({"role": "user", "message": user_question})
    render_chat_history()
    
    with st.spinner("Thinking..."):
        # Pathway 1: Media Chat (Direct Gemini Call)
        if 'active_media_file' in st.session_state:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content([st.session_state['active_media_file'], user_question])
            answer = response.text
            
        # Pathway 2: RAG Text Chat
        elif 'rag_pipeline' in st.session_state:
            rag = st.session_state['rag_pipeline']
            answer = rag.run(user_question)
            
        else:
            answer = "Please upload a file first."

    st.session_state.chat_history.append({"role": "assistant", "message": answer})
    render_chat_history()
