import google.generativeai as genai

def generate_flashcards(text, num_cards=10, api_key=None):
    """
    Generates Q&A flashcards from the given text using Gemini.
    Returns a list of dictionaries: [{'question': '...', 'answer': '...'}, ...]
    """
    if not api_key:
        raise ValueError("API Key is required")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    You are a helpful study assistant. Create {num_cards} flashcards based on the following text.
    
    Rules:
    1. Output strictly valid CSV format.
    2. Two columns: Question,Answer
    3. No header row.
    4. Escape quotes if necessary so the CSV is valid.
    5. No markdown formatting (no ```csv blocks).
    
    TEXT:
    {text[:50000]}  # Limit context to avoid errors, though 2.0 has 1M context.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up if model adds markdown blocks by mistake
        if content.startswith("```"):
            content = content.replace("```csv", "").replace("```", "").strip()
            
        cards = []
        lines = content.split('\n')
        for line in lines:
            # Simple splitter, but for robust CSV handling we might want the csv module. 
            # Given the strict prompt, this usually works for simple Q&A.
            # Let's use flexible split to handle potential commas in text.
            parts = line.split(',')
            if len(parts) >= 2:
                # Re-join answer parts if they contained commas
                q = parts[0].strip()
                a = ",".join(parts[1:]).strip()
                cards.append({"question": q, "answer": a})
                
        return cards, content # Return raw CSV content for download too
        
    except Exception as e:
        return [], f"Error generating flashcards: {str(e)}"
