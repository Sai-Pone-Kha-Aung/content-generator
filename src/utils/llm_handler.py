import google.generativeai as genai
import requests
import json
from typing import Optional, Dict, Any
from loguru import logger
from config.config import settings

class LLMHandler:
    def __init__(self):
        self.setup_gemini()
        self.setup_ollama()
        
    def setup_gemini(self):
        """Setup Google Gemini API client."""
        try:
            if settings.gemini_api_key:
                genai.configure(api_key=settings.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                logger.info("Google Gemini model initialized successfully.")
            else:
                logger.warning("Google Gemini API key is not set.")
        except Exception as e:
            logger.error(f"Failed to initialize Google Gemini client: {e}")
    
    def setup_ollama(self):
        """Setup Ollama API client."""
        try:
            response = requests.get(f"{settings.ollama_base_url}/api/tags")
            if response.status_code == 200:
                self.ollama_available = True
                logger.info("Ollama connection established.")
            else:
                self.ollama_available = False
                logger.warning("Ollama not available.")
        except Exception as e:
            self.ollama_available = False
            logger.error(f"Failed to initialize Ollama client: {e}")
    
    def generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate text using Google Gemini."""
        
        try:
            if not settings.gemini_api_key:
                raise ValueError("Google Gemini API key is not set.")
        
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating text with Google Gemini: {e}")
            return None
    
    def generate_with_ollama(self, prompt: str) -> Optional[str]:
        """Generate text using Ollama."""
        try:
            if not self.ollama_available:
                raise ValueError("Ollama not available.")
            
            payload = {
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": False,
            }
            
            response = requests.post(
                f"{settings.ollama_base_url}/api/generate",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return None
        
    def generate_content(self, prompt: str, provider: str = "gemini") -> Optional[str]:
        """Generate content using the specified provider."""
        
        logger.info(f"Generating content with {provider} provider.")
        if provider.lower() == "gemini":
            return self.generate_with_gemini(prompt)
        elif provider == "ollama":
            return self.generate_with_ollama(prompt)
        else:
            #Try gemini first, fallback to Ollama ... 
            content = self.generate_with_gemini(prompt)
            if content is None:
                logger.info("Gemini failed, trying Ollama...")
                content = self.generate_with_ollama(prompt)
            return content