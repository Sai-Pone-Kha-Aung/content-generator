import streamlit as st
from datetime import datetime
import json
from typing import Dict, Any

def initialize_session_state():
    """Initialize session state variables"""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = []

    if 'agent_initialized' not in st.session_state:
        st.session_state.agent_initialized = False

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        return timestamp
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def export_content_history():
    """Export content generation history"""
    if 'generated_content' not in st.session_state:
        return None

    export_data = []
    for content in st.session_state.generated_content:
        export_item = content.copy()
        export_item['timestamp'] = format_timestamp(content['timestamp'])
        export_data.append(export_item)

    return json.dumps(export_data, indent=2)

def validate_api_keys():
    """Validate that required API keys are present"""
    from config.config import settings

    missing_keys = []

    if not settings.gemini_api_key:
        missing_keys.append("GEMINI_API_KEY")

    if not settings.notion_token:
        missing_keys.append("NOTION_TOKEN")

    if not settings.notion_database_id:
        missing_keys.append("NOTION_DATABASE_ID")

    return missing_keys

def show_api_key_warning():
    """Show warning about missing API keys"""
    missing_keys = validate_api_keys()

    if missing_keys:
        st.error(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        st.info("Please check the Settings page for setup instructions.")
        return False

    return True
