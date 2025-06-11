import re
from typing import Dict, List, Tuple

def validate_gemini_api_key(api_key: str) -> Tuple[bool, str]:
    """Validate Gemini API key format"""
    if not api_key:
        return False, "API key is required"
    
    if not api_key.startswith('AIza'):
        return False, "Gemini API key should start with 'AIza'"
    
    if len(api_key) < 30:
        return False, "API key appears to be too short"
    
    return True, "Valid format"

def validate_notion_token(token: str) -> Tuple[bool, str]:
    """Validate Notion token format"""
    if not token:
        return False, "Notion token is required"
    
    if not token.startswith('secret_') and not token.startswith('ntn_'):
        return False, "Notion token should start with 'secret_' or 'ntn_'"
    
    if len(token) < 40:
        return False, "Token appears to be too short"
    
    return True, "Valid format"

def validate_notion_database_id(db_id: str) -> Tuple[bool, str]:
    """Validate Notion database ID format"""
    if not db_id:
        return False, "Database ID is required"
    
    # Remove hyphens for validation
    clean_id = db_id.replace('-', '')
    
    if len(clean_id) != 32:
        return False, "Database ID should be 32 characters (with or without hyphens)"
    
    if not re.match(r'^[a-f0-9]+$', clean_id):
        return False, "Database ID should contain only hexadecimal characters"
    
    return True, "Valid format"

def validate_ollama_url(url: str) -> Tuple[bool, str]:
    """Validate Ollama URL format"""
    if not url:
        return False, "Ollama URL is required"
    
    if not url.startswith('http://') and not url.startswith('https://'):
        return False, "URL should start with http:// or https://"
    
    return True, "Valid format"

def validate_ollama_model(model: str) -> Tuple[bool, str]:
    """Validate Ollama model name"""
    if not model:
        return False, "Model name is required"
    
    if len(model.strip()) < 2:
        return False, "Model name is too short"
    
    return True, "Valid format"

def validate_all_settings(settings: Dict) -> Dict[str, Tuple[bool, str]]:
    """Validate all settings and return results"""
    results = {}
    
    if 'gemini_api_key' in settings:
        results['gemini_api_key'] = validate_gemini_api_key(settings['gemini_api_key'])
    
    if 'notion_token' in settings:
        results['notion_token'] = validate_notion_token(settings['notion_token'])
    
    if 'notion_database_id' in settings:
        results['notion_database_id'] = validate_notion_database_id(settings['notion_database_id'])
    
    if 'ollama_base_url' in settings:
        results['ollama_base_url'] = validate_ollama_url(settings['ollama_base_url'])
    
    if 'ollama_model' in settings:
        results['ollama_model'] = validate_ollama_model(settings['ollama_model'])
    
    return results

def get_validation_summary(validation_results: Dict[str, Tuple[bool, str]]) -> Tuple[bool, List[str]]:
    """Get a summary of validation results"""
    all_valid = True
    errors = []
    
    for field, (is_valid, message) in validation_results.items():
        if not is_valid:
            all_valid = False
            errors.append(f"{field.replace('_', ' ').title()}: {message}")
    
    return all_valid, errors
