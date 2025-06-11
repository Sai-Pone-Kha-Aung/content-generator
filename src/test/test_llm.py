import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.llm_handler import LLMHandler

def test_llm():
    llm = LLMHandler()
    
    prompt = "Write a short blog post about the benefits of AI in content creation."
    
    print("Testing Google Gemini generation...")
    content_gemini = llm.generate_content(prompt, "gemini")
    if content_gemini:
        print("✅ Gemini working!")
        print(f"Content preview: {content_gemini[:100]}...")
    else:
        print("❌ Gemini failed")
        
    print("\nTesting Ollama...")
    content_ollama = llm.generate_content(prompt, "ollama")
    if content_ollama:
        print("✅ Ollama working!")
        print(f"Content preview: {content_ollama[:100]}...")
    else:
        print("❌ Ollama failed")

if __name__ == "__main__":
    test_llm()