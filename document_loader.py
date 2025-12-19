from pypdf import PdfReader
from PIL import Image
import pytesseract


def load_document(file):
    """Loads text from a PDF, PNG, or TXT file."""
    if file.size == 0:
        raise ValueError("The uploaded file is empty.")

    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "image/png":
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        return text
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF, PNG, or TXT file.")
