from typing import Dict, List, Optional
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.llm_handler import LLMHandler
from src.notion_handler import NotionHandler
from src.prompt_engine import PromptEngine, ContentRequest, ContentType, ToneType, LengthType
from src.template_manager import TemplateManager
from config.config import settings

console = Console()

class EnhancedContentAgent:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.notion_handler = NotionHandler()
        self.prompt_engine = PromptEngine()
        self.template_manager = TemplateManager()
        logger.info("Enhanced Content Agent initialized")
    
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
                    call_to_