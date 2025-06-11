import streamlit as st
import sys
import os
from pathlib import Path
import time
from datetime import datetime
import pandas as pd
# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.core.content_agent import ContentAgent
from src.components.components import (
    render_content_form,
    show_success_message,
    show_error_message,
    render_system_health,
    render_content_stats,
    render_content_table
)

def show_content_generator():
    """Content Generation Page"""
    st.header("📝 Content Generator")
    """Initialize session state"""
    if 'agent' not in st.session_state:
        with st.spinner("Initializing AI Content Agent..."):
            try:
                st.session_state.agent = ContentAgent()
                st.success("✅ AI Content Agent initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize agent: {str(e)}")
                st.stop()

    form_data = render_content_form()
    
    if form_data['submitted']:
        if not form_data['topic']:
            st.error("❌ Topic is required to generate content.")
            return
        
        #Show generation progress
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        try:
            with st.spinner("🤖 Generating content..."):
                # Create enhanced prompt if custom instructions provided
                topic = form_data['topic']
                if form_data['custom_prompt']:
                    topic += f"\n\nAdditional instructions: {form_data['custom_prompt']}"
                if form_data['target_audience']:
                    topic += f"\n\nTarget audience: {form_data['target_audience']}"

                result = st.session_state.agent.generate_and_save_content(
                    topic=topic,
                    content_type=form_data['content_type'],
                    ai_provider=form_data['ai_provider'],
                    tone=form_data['tone'],
                    length=form_data['length']
                )

            if result:
                # Store in session state for later reference
                if 'generated_content' not in st.session_state:
                    st.session_state.generated_content = []

                result['timestamp'] = datetime.now()
                st.session_state.generated_content.append(result)

                # Show success message
                show_success_message(
                    title=result['title'],
                    content_preview=result['content_preview'],
                    stats={
                        'word_count': result['word_count'],
                        'tags': result['tags'],
                        'ai_provider': result['ai_provider']
                    }
                )

                # Show Notion link
                st.info(f"💾 Content saved to Notion. Page ID: `{result['notion_page_id']}`")

            else:
                show_error_message("Failed to generate or save content. Please check system status.")

        except Exception as e:
            show_error_message(f"An error occurred: {str(e)}")
            
    # Show recent generations
    if 'generated_content' in st.session_state and st.session_state.generated_content:
        st.markdown("---")
        st.subheader("📚 Recent Generations")

        # Show last 5 generations
        recent_content = st.session_state.generated_content[-5:]
        for i, content in enumerate(reversed(recent_content)):
            with st.expander(f"📄 {content['title']} ({content['timestamp'].strftime('%H:%M:%S')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Word Count:** {content['word_count']}")
                    st.write(f"**AI Provider:** {content['ai_provider'].title()}")
                with col2:
                    st.write(f"**Tags:** {', '.join(content['tags'])}")
                    st.write(f"**Notion ID:** `{content['notion_page_id']}`")

def show_content_library():
    """Content Library Page"""
    
    st.header("📚 Content Library")

    if 'agent' not in st.session_state:
        st.warning("⚠️ Please initialize the agent from the Content Generator page first.")
        return
    try:
        with st.spinner("📖 Loading content from Notion..."):
            #Get recent pages from Notion
            if 'agent' in st.session_state:
                recent_pages = st.session_state.agent.notion_handler.list_recent_pages(limit=20)
            else:
                # Initialize agent if not available
                from src.core.content_agent import ContentAgent
                agent = ContentAgent()
                recent_pages = agent.notion_handler.list_recent_pages(limit=20)
        if recent_pages:
            st.success(f"✅ Found {len(recent_pages)} content items")
            
            #Process pages for display
            content_data = []
            for page in recent_pages:
                try:
                    properties = page.get('properties', {})
                    
                    #Safe property extraction
                    title = "Untitled"
                    if 'Title' in properties and properties['Title'].get('title'):
                         title = properties['Title']['title'][0]['text']['content']
                         
                    status = "Unknown"
                    if 'Status' in properties and properties['Status'].get('select'):
                        status = properties['Status']['select']['name']

                    content_type = "Unknown"
                    if 'Type' in properties and properties['Type'].get('select'):
                        content_type = properties['Type']['select']['name']
                        
                    word_count = 0
                    if 'Word Count' in properties and properties['Word Count'].get('number') is not None:
                        word_count = properties['Word Count']['number']

                    ai_provider = "Unknown"
                    if 'AI Model Used' in properties and properties['AI Model Used'].get('rich_text'):
                        if properties['AI Model Used']['rich_text']:
                            ai_provider = properties['AI Model Used']['rich_text'][0]['text']['content']

                    created = page.get('created_time', '')
                    
                    content_data.append({
                        'title': title,
                        'status': status,
                        'type': content_type,
                        'word_count': word_count,
                        'ai_provider': ai_provider,
                        'created': created,
                        'notion_page_id': page['id']
                    })
                except Exception as e:
                    st.warning(f"Error processing page {page.get('id', 'unknown')}: {e}")
                    # Add debug info
                    st.write("Page properties:", list(page.get('properties', {}).keys()))
                    continue
            # Display content table
            render_content_table(content_data)
            
            #Content Statistics
            if content_data:
                st.markdown("---")
                st.subheader("📊 Content Statistics")

                df = pd.DataFrame(content_data)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Content Items", len(content_data))
                
                with col2:
                    total_words = df['word_count'].sum()
                    st.metric("Total Words", f"{total_words:,}")
                    
                with col3:
                    avg_words = df['word_count'].mean()
                    st.metric("Average Words per Item", f"{avg_words:.2f}")
                with col4:
                    draft_count = len(df[df['status'] == 'Draft'])
                    st.metric("Drafts", draft_count)
                
                #Charts
                col1, col2 = st.columns(2)
                with col1:
                    #Content Type Distribution
                    if 'type' in df.columns:
                        type_counts = df['type'].value_counts()
                        if not type_counts.empty:
                            st.subheader("Content Types")
                            st.bar_chart(type_counts)
                        
                with col2:
                    # AI provider usage
                    if 'ai_provider' in df.columns:
                        provider_counts = df['ai_provider'].value_counts()
                        if not provider_counts.empty:
                            st.subheader("AI Provider Usage")
                            st.bar_chart(provider_counts)
        else:
            st.info("📝 No content found in your Notion database yet. Generate some content to see it here!")
            # Add debug info
            st.write("Debug: list_recent_pages returned:", recent_pages)

    except Exception as e:
        show_error_message(f"Failed to load content library: {str(e)}")

def show_system_status():
    """System Status Page"""
    st.header("🔧 System Status")

    if 'agent' not in st.session_state:
        with st.spinner("Initializing AI Content Agent..."):
            try:
                st.session_state.agent = ContentAgent()
                st.success("✅ AI Content Agent initialized for status check!")
            except Exception as e:
                st.error(f"❌ Failed to initialize agent: {str(e)}")
                st.stop()

    with st.spinner("🔍 Checking system status..."):
        try:
            # Test LLM providers with proper error handling
            try:
                gemini_test = st.session_state.agent.llm_handler.generate_content("Test", "gemini") is not None
            except Exception as e:
                st.warning(f"Gemini test failed: {e}")
                gemini_test = False
                
            try:
                ollama_test = st.session_state.agent.llm_handler.generate_content("Test", "ollama") is not None
            except Exception as e:
                st.warning(f"Ollama test failed: {e}")
                ollama_test = False

            # # Test Notion
            # try:
            #     notion_test = st.session_state.agent.notion_handler.test_connection()
            #     st.success(f"✅ Notion test result: {notion_test}")
            # except Exception as e:
            #     st.error(f"❌ Notion test failed with exception: {str(e)}")
            #     notion_test = False
            
            llm_status = {
                'gemini': gemini_test,
                'ollama': ollama_test
            }

            render_system_health(llm_status)

            # Detailed status
            st.markdown("---")
            st.subheader("🔍 Detailed Status")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🤖 AI Providers")

                if gemini_test:
                    st.success("✅ Gemini API: Connected and working")
                else:
                    st.error("❌ Gemini API: Failed to connect")

                if ollama_test:
                    st.success("✅ Ollama: Connected and working")
                else:
                    st.error("❌ Ollama: Failed to connect or not running")

            # with col2:
            #     st.markdown("### 💾 Storage")

            #     if notion_test:
            #         st.success("✅ Notion API: Connected")
            #         # Get database info
            #         try:
            #             db_structure = st.session_state.agent.notion_handler.get_database_structure()
            #             st.info(f"📊 Database properties: {len(db_structure)} configured")
            #         except:
            #             st.warning("⚠️ Could not retrieve database structure")
            #     else:
            #         st.error("❌ Notion API: Connection failed")

            # System recommendations
            st.markdown("---")
            st.subheader("💡 Recommendations")

            if not gemini_test and not ollama_test:
                st.error("🚨 No AI providers available. Please check your API keys and Ollama installation.")
            elif not gemini_test:
                st.warning("⚠️ Gemini API not available. Content generation will use Ollama only.")
            elif not ollama_test:
                st.warning("⚠️ Ollama not available. Content generation will use Gemini only.")
            else:
                st.success("🎉 All AI providers are working correctly!")

            # if not notion_test:
            #     st.error("🚨 Notion integration not working. Generated content cannot be saved.")
            # else:
            #     st.success("💾 Notion integration is working correctly!")

        except Exception as e:
            show_error_message(f"System status check failed: {str(e)}")

def show_settings():
    """Settings Page"""
    
    st.header("⚙️ Settings")
    st.markdown("Configure your API keys and system preferences")
    
    # Information Section
    with st.expander("ℹ️ Setup Information", expanded=False):
        st.markdown("""
        ### Getting Started
        
        To use the AI Content Generator, you'll need to set up the following:
        
        #### 1. Google Gemini API 🤖
        - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        - Create a new API key
        - Copy and paste it into the Gemini API Key field below
        
        #### 2. Notion Integration 📝
        - Go to [Notion Integrations](https://www.notion.so/my-integrations)
        - Create a new integration
        - Copy the "Internal Integration Token"
        - Create a database in Notion with these properties:
          - **Title** (Title type)
          - **Content** (Text type)
          - **Type** (Select type)
          - **Status** (Select type)
          - **AI Model Used** (Text type)
          - **Word Count** (Number type)
          - **Tags** (Multi-select type)
        - Share your database with the integration
        - Copy the database ID from the URL
        
        #### 3. Ollama (Optional) 🦙
        - Install Ollama from [ollama.ai](https://ollama.ai)
        - Pull a model: `ollama pull llama3.1`
        - Make sure Ollama is running on your system
        
        #### 4. Save Settings
        - Fill in the API keys and configuration below
        - Click "Save Settings" to persist your configuration
        - Test your connections to ensure everything works
        """)
    

    # Initialize session state for settings if not exists
    if 'user_settings' not in st.session_state:
        # Load current settings from config
        from config.config import settings
        st.session_state.user_settings = {
            'gemini_api_key': settings.gemini_api_key,
            'notion_token': settings.notion_token,
            'notion_database_id': settings.notion_database_id,
            'ollama_base_url': settings.ollama_base_url,
            'ollama_model': settings.ollama_model
        }

    # API Configuration Section
    st.markdown("### 🔐 API Configuration")
    
    with st.form("api_settings_form"):
        st.markdown("#### Google Gemini API")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            gemini_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.user_settings.get('gemini_api_key', ''),
                type="password",
                help="Get your API key from Google AI Studio",
                placeholder="Enter your Gemini API key"
            )
            
            # Real-time validation for Gemini API key
            if gemini_key:
                from src.utils.settings_validator import validate_gemini_api_key
                is_valid, message = validate_gemini_api_key(gemini_key)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")
        
        with col2:
            st.markdown("**Get API Key:**")
            st.markdown("[Google AI Studio](https://makersuite.google.com/app/apikey)")
        
        st.markdown("#### Notion Integration")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            notion_token = st.text_input(
                "Notion API Token",
                value=st.session_state.user_settings.get('notion_token', ''),
                type="password",
                help="Create an integration at Notion Developer Portal",
                placeholder="Enter your Notion API token"
            )
            
            # Real-time validation for Notion token
            if notion_token:
                from src.utils.settings_validator import validate_notion_token
                is_valid, message = validate_notion_token(notion_token)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")
            
            notion_db_id = st.text_input(
                "Notion Database ID",
                value=st.session_state.user_settings.get('notion_database_id', ''),
                help="ID of your Notion database for storing content",
                placeholder="Enter your Notion database ID"
            )
            
            # Real-time validation for Notion database ID
            if notion_db_id:
                from src.utils.settings_validator import validate_notion_database_id
                is_valid, message = validate_notion_database_id(notion_db_id)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")
        
        with col2:
            st.markdown("**Setup Notion:**")
            st.markdown("1. [Create Integration](https://www.notion.so/my-integrations)")
            st.markdown("2. Copy database ID from URL")
            st.markdown("3. Share database with integration")

        st.markdown("#### Ollama Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            ollama_url = st.text_input(
                "Ollama Base URL",
                value=st.session_state.user_settings.get('ollama_base_url', 'http://localhost:11434'),
                help="URL where Ollama is running",
                placeholder="http://localhost:11434"
            )
            
            # Real-time validation for Ollama URL
            if ollama_url:
                from src.utils.settings_validator import validate_ollama_url
                is_valid, message = validate_ollama_url(ollama_url)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")
        
        with col2:
            ollama_model = st.text_input(
                "Ollama Model",
                value=st.session_state.user_settings.get('ollama_model', 'llama3.1'),
                help="Name of the Ollama model to use",
                placeholder="llama3.1"
            )
            
            # Real-time validation for Ollama model
            if ollama_model:
                from src.utils.settings_validator import validate_ollama_model
                is_valid, message = validate_ollama_model(ollama_model)
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⚠️ {message}")

        # Save Settings Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            save_settings = st.form_submit_button(
                "💾 Save Settings",
                type="primary",
                use_container_width=True
            )

        # Handle form submission
        if save_settings:
            # Validate settings before saving
            from src.utils.settings_validator import validate_all_settings, get_validation_summary
            
            settings_to_validate = {
                'gemini_api_key': gemini_key,
                'notion_token': notion_token,
                'notion_database_id': notion_db_id,
                'ollama_base_url': ollama_url,
                'ollama_model': ollama_model
            }
            
            validation_results = validate_all_settings(settings_to_validate)
            is_valid, errors = get_validation_summary(validation_results)
            
            if not is_valid:
                st.error("❌ Validation failed:")
                for error in errors:
                    st.error(f"• {error}")
            else:
                # Update session state
                st.session_state.user_settings.update({
                    'gemini_api_key': gemini_key,
                    'notion_token': notion_token,
                    'notion_database_id': notion_db_id,
                    'ollama_base_url': ollama_url,
                    'ollama_model': ollama_model
                })
                
                # Update environment variables for current session
                os.environ['GEMINI_API_KEY'] = gemini_key
                os.environ['NOTION_API_KEY'] = notion_token
                os.environ['NOTION_DATABASE_ID'] = notion_db_id
                os.environ['OLLAMA_BASE_URL'] = ollama_url
                os.environ['OLLAMA_MODEL'] = ollama_model
                
                # Save to .env file for persistence
                from config.config import save_settings_to_env
                save_success = save_settings_to_env(st.session_state.user_settings)
                
                # Reinitialize settings
                from config.config import settings
                settings.update_from_dict(st.session_state.user_settings)
                
                # Clear agent from session state to force reinitialization
                if 'agent' in st.session_state:
                    del st.session_state['agent']
                
                if save_success:
                    st.success("✅ Settings saved successfully to .env file! Please reinitialize the agent from the Content Generator page.")
                else:
                    st.warning("⚠️ Settings updated for current session, but couldn't save to .env file. Changes may not persist after restart.")
                st.balloons()

    # Connection Status Section
    st.markdown("---")
    st.markdown("### 🔍 Connection Status")
    
    if st.button("🧪 Test Connections", type="secondary"):
        with st.spinner("Testing connections..."):
            # Test API connections with current settings
            test_results = {}
            
            # Test Gemini
            if st.session_state.user_settings.get('gemini_api_key'):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=st.session_state.user_settings['gemini_api_key'])
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content("Test")
                    test_results['gemini'] = True
                except:
                    test_results['gemini'] = False
            else:
                test_results['gemini'] = False
            
            # Test Ollama
            if st.session_state.user_settings.get('ollama_base_url'):
                try:
                    import requests
                    response = requests.get(f"{st.session_state.user_settings['ollama_base_url']}/api/tags", timeout=5)
                    test_results['ollama'] = response.status_code == 200
                except:
                    test_results['ollama'] = False
            else:
                test_results['ollama'] = False
            
            # Test Notion
            if st.session_state.user_settings.get('notion_token') and st.session_state.user_settings.get('notion_database_id'):
                try:
                    from notion_client import Client
                    client = Client(auth=st.session_state.user_settings['notion_token'])
                    client.databases.retrieve(database_id=st.session_state.user_settings['notion_database_id'])
                    test_results['notion'] = True
                except:
                    test_results['notion'] = False
            else:
                test_results['notion'] = False
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "✅ Connected" if test_results.get('gemini') else "❌ Failed"
            st.markdown(f"**Gemini API:** {status}")
        
        with col2:
            status = "✅ Connected" if test_results.get('ollama') else "❌ Failed"
            st.markdown(f"**Ollama:** {status}")
        
        with col3:
            status = "✅ Connected" if test_results.get('notion') else "❌ Failed"
            st.markdown(f"**Notion:** {status}")

    # Current Configuration Display
    with st.expander("📋 Current Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API Keys Status:**")
            gemini_status = "✅ Set" if st.session_state.user_settings.get('gemini_api_key') else "❌ Not Set"
            notion_token_status = "✅ Set" if st.session_state.user_settings.get('notion_token') else "❌ Not Set"
            notion_db_status = "✅ Set" if st.session_state.user_settings.get('notion_database_id') else "❌ Not Set"
            
            st.markdown(f"- Gemini API Key: {gemini_status}")
            st.markdown(f"- Notion Token: {notion_token_status}")
            st.markdown(f"- Notion Database ID: {notion_db_status}")
        
        with col2:
            st.markdown("**Ollama Configuration:**")
            st.markdown(f"- Base URL: `{st.session_state.user_settings.get('ollama_base_url', 'Not Set')}`")
            st.markdown(f"- Model: `{st.session_state.user_settings.get('ollama_model', 'Not Set')}`")

    # Content Templates
    with st.expander("📝 Content Templates"):
        st.markdown("**Available Content Types:**")
        templates = {
            "Blog": "Long-form articles with SEO optimization",
            "Social": "Short, engaging social media posts",
            "Article": "Professional articles and documentation",
            "Marketing": "Persuasive marketing copy and ads"
        }

        for template_type, description in templates.items():
            st.markdown(f"- **{template_type}:** {description}")

    # Usage Statistics
    if 'generated_content' in st.session_state:
        with st.expander("📊 Usage Statistics"):
            content_count = len(st.session_state['generated_content'])
            st.metric("Content Generated This Session", content_count)
            
            if content_count > 0:
                total_words = sum(item['word_count'] for item in st.session_state['generated_content'])
                st.metric("Total Words Generated", f"{total_words:,}")
    
    # Data Management
    st.markdown("---")
    st.subheader("🗑️ Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Session", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Session reset successfully!")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Generated Content", type="secondary"):
            if 'generated_content' in st.session_state:
                del st.session_state['generated_content']
                st.success("✅ Generated content history cleared!")

        