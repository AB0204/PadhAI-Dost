from pypdf import PdfReader
from PIL import Image
import pytesseract
import os
import mimetypes

def load_document(file_path):
    """Loads text from a PDF, PNG, or TXT file path."""
    
    if not os.path.exists(file_path):
        raise ValueError("File does not exist.")
        
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValueError("The uploaded file is empty.")

    # Guess MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type == "application/pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
        
    elif mime_type == "image/png" or mime_type == "image/jpeg":
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
        
    elif mime_type == "text/plain":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
            
    else:
        # Fallback based on extension if mime detection fails or is generic
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
             reader = PdfReader(file_path)
             text = ""
             for page in reader.pages:
                 text += page.extract_text()
             return text
        elif ext == ".txt":
             with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        
        raise ValueError(f"Unsupported file type ({mime_type} / {ext}). Please upload a PDF, PNG, or TXT file.")
