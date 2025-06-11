import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd

def render_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """
    Renders a metric card with optional delta and help text.
    """
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )

def render_system_health(llm_status: Dict):
    """
    Renders the system health status.
    """
    
    st.subheader("System Health")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        gemini_status = "🟢 Online" if llm_status.get('gemini') else "🔴 Offline"
        st.markdown(f"**Gemini API:** {gemini_status}")

    with col2:
        ollama_status = "🟢 Online" if llm_status.get('ollama') else "🔴 Offline"
        st.markdown(f"**Ollama API:** {ollama_status}")
        
    # with col3:
    #     notion_status_text = "🟢 Connected" if notion_status else "Disconnected"
    #     st.markdown(f"**Notion API:** {notion_status_text}"
    # )

def render_content_preview(content: str, max_length: int = 300):
    """
    Renders a preview of the content.
    """
    
    if len(content) > max_length:
        preview = content[:max_length] + "..."
        with st.expander("📄 Content Preview"):
            st.text_area("Preview", preview, height=100, disabled=True)
            if st.button("Show Full Content"):
                st.text_area("Full Content", content, height=400, disabled=True)
    else:
        st.text_area("Content", content, height=200, disabled=True)

def render_progress_bar(current: int, total:int, label: str):
    """
    Renders a progress bar.
    """
    
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"{label}: {current}/{total}")
    
def render_content_stats(stats: Dict):
    """
    Renders content statistics.
    """
    
    if not stats:
        st.info("No content statistics available.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        #Content type pie chart
        if 'content_types' in stats:
            fig_pie = px.pie(
                values=stats['content_types'].values(),
                names=stats['content_types'].keys(),
                title ="Content Types Distribution",
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with col2:
        #AI provider bar chart
        if 'ai_providers' in stats:
            fig_bar = px.bar(
                x=list(stats['ai_providers'].keys()),
                y=list(stats['ai_providers'].values()),
                title="AI Provider Usage",
                labels={'x': 'AI Provider', 'y': 'Usage Count'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
def render_content_form():
    """
    Renders a form for content generation.
    """
    
    with st.form("content_form"):
        st.subheader("📝 Content Configuration")
       
        col1, col2 = st.columns(2)
       
        with col1:
            topic = st.text_input(
                "Content Topic*",
                placeholder="e.g,.Benefits of AI in Marketing",
                help="Main topic or theme for the content."
            )
            
            content_type = st.selectbox(
                    "Content Type*",
                    options=["Blog Post", "Social Media Post", "Email Newsletter", "Video Script"],
                    help="Type of content to generate."
            )
            
            length = st.selectbox(
                "Content Length",
                    ["Short", "Medium", "Long"],
                    index=1,
                    help="Short: 200-400 words, Medium: 500-800 words, Long: 1000+ words"
            )
            
        with col2:
                ai_provider = st.selectbox(
                    "AI Provider",
                    options=["Gemini", "Ollama"],
                    help="Select the AI provider for content generation."
                )
                
                tone = st.selectbox(
                    "Tone",
                    options=["Professional", "Casual", "Friendly", "Formal", "Creative"],
                    help="Tone of the content."
                )
                
                #Advance settings
                with st.expander("🔧 Advanced Options"):
                    custom_prompt = st.text_area(
                        "Custom Instructions(Optional)",
                        placeholder="Optional custom prompt for the AI model.",
                        help="You can provide a custom prompt to guide the AI in generating content.",
                        height=100
                    )
                    
                    target_audience = st.text_input(
                        "Target Audience",
                        placeholder="e.g,.Marketing Professionals, Small Business Owners",
                        help="Define the target audience for the content."
                    )
            
        #Tags input
        st.markdown("**Tags (Optional)**")
        tags_input = st.text_input(
            "Tags",
            placeholder="AI, Technology, Innovation (Comma-separated)",
            help="Comma-separated tags to categorize the content.", 
            label_visibility="collapsed"
        )
        
        #submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submitted = st.form_submit_button(
                    "🚀 Generate Content",
                    type="primary",
                    use_container_width=True
                )
        
        return {
                'submitted': submitted,
                'topic': topic,
                'content_type': content_type.lower(),
                'length': length.lower(),
                'ai_provider': ai_provider.lower(),
                'tone': tone.lower(),
                'custom_prompt': custom_prompt,
                'target_audience': target_audience,
                'tags': [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
        }
    
def show_success_message(title: str, content_preview: str, stats: Dict):
      """Show success message with content details"""
      st.markdown('<div class="success-message">', unsafe_allow_html=True)
      st.markdown("### ✅ Content Generated Successfully!")
      st.markdown(f"**Title:** {title}")
      st.markdown(f"**Word Count:** {stats.get('word_count', 'N/A')}")
      st.markdown(f"**Tags:** {', '.join(stats.get('tags', []))}")
      st.markdown(f"**AI Provider:** {stats.get('ai_provider', 'N/A').title()}")
      st.markdown('</div>', unsafe_allow_html=True)
      
      #Content preview
      with st.expander("📄 Previce Generated Content"):
          st.text_area(
              "Content",
              content_preview,
              height=200,
              disabled=True,
          )

def show_error_message(error: str):
    """Show error message"""
    st.markdown('<div class="error-message">', unsafe_allow_html=True)
    st.markdown("### ❌ Error Occurred!")
    st.markdown(f"**Details:** {error}")
    st.markdown('</div>', unsafe_allow_html=True)
    
def render_content_table(content_list: List[Dict]):
    """
    Renders a table of generated content.
    """
    
    if not content_list:
        st.info("No content generated yet.")
        return
    
    df = pd.DataFrame(content_list)
    
    #Configure Columns
    columns_config = {
        "title": st.column_config.TextColumn("Title", width="large"),
        "type": st.column_config.TextColumn("Type", width="small"),
        "status": st.column_config.TextColumn("Status", width="small"),
        "word_count": st.column_config.NumberColumn("Words", width="small"),
        "created": st.column_config.DatetimeColumn("Created", width="medium"),
        "ai_provider": st.column_config.TextColumn("AI Provider", width="small")
    }
    
    st.dataframe(
        df,
        column_config=columns_config,
        use_container_width=True,
        hide_index=True,
    )