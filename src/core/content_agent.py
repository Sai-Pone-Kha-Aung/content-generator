from typing import Dict, List, Optional
from loguru import logger
import re
from src.prompt.prompt_engine import ContentType, LengthType, PromptEngine, ContentRequest, ToneType
from src.utils.llm_handler import LLMHandler
from src.utils.notion_handler import NotionHandler
from config.config import settings
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.template.template_manager import TemplateManager
console = Console()

class ContentAgent:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.notion_handler = NotionHandler()
        self.prompt_engine = PromptEngine()
        self.template_manager = TemplateManager()
        logger.info("Content Agent initialized")

    def generate_content_with_advanced_prompts(self,
                                             topic: str,
                                             content_type: str = "blog",
                                             ai_provider: str = "gemini",
                                             tone: str = "professional",
                                             length: str = "medium",
                                             target_audience: str = None,
                                             keywords: List[str] = None,
                                             industry: str = None,
                                             custom_instructions: str = None,
                                             include_examples: bool = False,
                                             seo_focused: bool = False,
                                             call_to_action: str = None,
                                             brand_voice: str = None) -> Optional[Dict]:
        """Generate content using advanced prompt engineering"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Create enhanced content request
            task1 = progress.add_task("Preparing advanced prompt...", total=None)
            
            try:
                content_request = ContentRequest(
                    topic=topic,
                    content_type=ContentType(content_type.lower()),
                    tone=ToneType(tone.lower()),
                    length=LengthType(length.lower()),
                    target_audience=target_audience,
                    keywords=keywords or [],
                    industry=industry,
                    custom_instructions=custom_instructions,
                    include_examples=include_examples,
                    seo_focused=seo_focused,
                    call_to_action=call_to_action,
                    brand_voice=brand_voice
                )
                progress.update(task1, description="Prompt prepared")
            except Exception as e:
                logger.error(f"Error preparing prompt: {e}")
                return None
