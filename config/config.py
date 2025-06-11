from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
    
    #API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    notion_token: str = os.getenv("NOTION_API_KEY", "")
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID", "")
    
    #ollama settings
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    #Content Generation Settings
    max_content_length: int = 2000
    default_content_type: str = "blog"
    
    def update_from_dict(self, settings_dict: dict):
        """Update settings from a dictionary"""
        for key, value in settings_dict.items():
            if hasattr(self, key) and value:
                setattr(self, key, value)

def save_settings_to_env(settings_dict: dict):
    """Save settings to .env file"""
    try:
        # Read existing .env file
        env_path = ".env"
        env_lines = []
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_lines = f.readlines()
        
        # Create a mapping of existing variables
        existing_vars = {}
        for i, line in enumerate(env_lines):
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                existing_vars[key] = i
        
        # Update or add new variables
        env_mapping = {
            'gemini_api_key': 'GEMINI_API_KEY',
            'notion_token': 'NOTION_API_KEY',
            'notion_database_id': 'NOTION_DATABASE_ID',
            'ollama_base_url': 'OLLAMA_BASE_URL',
            'ollama_model': 'OLLAMA_MODEL'
        }
        
        for key, value in settings_dict.items():
            if key in env_mapping and value:
                env_key = env_mapping[key]
                new_line = f"{env_key}={value}\n"
                
                if env_key in existing_vars:
                    # Update existing line
                    env_lines[existing_vars[env_key]] = new_line
                else:
                    # Add new line
                    env_lines.append(new_line)
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            f.writelines(env_lines)
        
        return True
    except Exception as e:
        print(f"Error saving to .env file: {e}")
        return False
        
settings = Settings()