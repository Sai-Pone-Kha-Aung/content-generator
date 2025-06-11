import streamlit as st
import os
import sys
from pathlib import Path
from streamlit_option_menu import option_menu
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from src.pages.pages import (
    show_content_generator,
    show_content_library,
    show_system_status,
    show_settings
)

#Page Configuration
st.set_page_config(
    page_title="AI Content Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

#CSS
st.markdown("""
<style>
    .main-header {
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e6e9ef;
        margin: 0.5rem 0;
    }

    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        color: #155724;
    }

    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        color: #721c24;
    }

    .info-box {
        padding: 1rem;
        background-color: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 0.375rem;
        color: #0d47a1;
        margin: 1rem 0;
    }
    
    .settings-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .api-status {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem 0;
    }
    
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-failed {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
            """, unsafe_allow_html=True)

def main():
    #Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🤖 AI Content Agent")
        st.markdown("*Generate high-quality content with AI and save it to your Notion*")
    
    with col2:
        if st.button("🔄 Refresh", type="secondary"):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{}" width="200">
        </div>
        """.format(
            __import__('base64').b64encode(open("public/Logo.png", "rb").read()).decode()
        ),
        unsafe_allow_html=True
    )
        
        selected = option_menu(
            menu_title = "Navigation",
            options = ["Content Generation", "Content Library", "System Status", "Settings"],
            icons = ["pencil-square", "book", "activity", "gear"],
            menu_icon = "robot",
            default_index = 0,
            styles = {
                "container": {
                    "padding": "20px",
                    "background-color": "#fafafa",
                    "icon": {
                        "color": "#4285f4",
                        "font-size": "1.5rem",
                    },
                    "nav-link": {
                        "font-size": "1.2rem",
                        "text-align": "left",
                        "margin": "0",
                        "--hover-color": "#eee"
                    },
                    "nav-link-selected": {
                        "background-color": "#4285f4",
                    },
                }
            }
        )
        
    if selected == "Content Generation":
        show_content_generator()
    elif selected == "Content Library":
        show_content_library()
    elif selected == "System Status":
        show_system_status()
    elif selected == "Settings":
        show_settings()



if __name__ == "__main__":
    main()