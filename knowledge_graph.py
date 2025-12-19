from langchain_google_genai import GoogleGenerativeAI
import graphviz

def generate_knowledge_graph(text, api_key):
    """
    Generates a Knowledge Graph using Graphviz DOT language from the given text.
    """
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    
    prompt = f"""
    You are an expert knowledge graph generator.
    Analyze the following text and create a concept map using Graphviz DOT syntax.
    
    Rules:
    1. Extract key concepts as nodes.
    2. Extract relationships as edges with labels (e.g., "A -> B [label='causes']").
    3. Keep labels concise (1-3 words).
    4. Limit the graph to the top 20 most important connections to avoid clutter.
    5. Output ONLY the valid DOT code inside a code block. Do not include markdown formatting like ```dot or ```. Just the raw code.
    
    Text:
    {text[:5000]} 
    
    (Note: Text truncated to 5000 chars for graph generation context)
    """
    
    response = llm.invoke(prompt)
    
    # Clean up response to ensure it's just DOT code
    dot_code = response.strip()
    if "```" in dot_code:
        dot_code = dot_code.replace("```dot", "").replace("```", "").strip()
        
    return dot_code
