from typing import Dict, List, Optional
from loguru import logger
import re
from src.utils.llm_handler import LLMHandler
from src.utils.notion_handler import NotionHandler
from config.config import settings
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
console = Console()

class ContentAgent:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.notion_handler = NotionHandler()
        logger.info("Content Agent initialized")
        
    def create_content_prompt(self, topic: str,
                              content_type: str,
                              tone: str = "professional",
                              length: str = "medium",
                              ) -> str:
        """
        Create a prompt for content generation based on the topic, content type, tone, and length.
        """
        length_guide = {
            "short": "200-400 words",
            "medium": "400-800 words",
            "long": "800-1500 words"
        }
        
        prompts = {
             "blog": f"""Write a {length_guide.get(length, '500-800 words')} blog post about "{topic}".
             Requirements:
             - Tone: {tone}
             - Include an engaging introduction
             - Use clear headings and subheadings
             - Provide actionable insights
             - End with a compelling conclusion
             - Make it SEO-friendly

            Topic: {topic} """,
            "social": f"""Create a social media post about "{topic}".

            Requirements:
            - Tone: {tone}
            - Length: {length_guide.get(length, '100-200 words')}
            - Include relevant hashtags
            - Make it engaging and shareable
            - Clear call-to-action

            Topic: {topic}""",
            "article": f"""Write a comprehensive article about "{topic}".

            Requirements:
            - Tone: {tone}
            - Length: {length_guide.get(length, '800-1200 words')}
            - Well-researched content
            - Professional structure
            - Include examples where relevant

            Topic: {topic}""",
            "article": f"""Write a comprehensive article about "{topic}".

            Requirements:
            - Tone: {tone}
            - Length: {length_guide.get(length, '800-1200 words')}
            - Well-researched content
            - Professional structure
            - Include examples where relevant

            Topic: {topic}""",

            "marketing": f"""Create marketing copy for "{topic}".

            Requirements:
            - Tone: {tone}
            - Length: {length_guide.get(length, '300-500 words')}
            - Persuasive and compelling
            - Focus on benefits
            - Include call-to-action
            - Target audience focused

            Topic: {topic}"""
        }
        
        return prompts.get(content_type.lower(), prompts["blog"])
    
    def extract_title_from_content(self, content: str) -> str:
        """Extract or generate title from content"""
        lines = content.strip().split('\n')

        # Look for markdown headings
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('## '):
                return line[3:].strip()

        # Look for lines that look like titles
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not line.startswith('*') and len(line) < 100:
                return line

        # Fallback: use first 50 characters
        return content[:50].strip() + "..."
    
    def extract_tags_from_content(self, content: str, topic: str) -> List[str]:
        """Extract relevant tags from content and topic"""
        tags = []

        # Add topic-based tags
        topic_words = topic.lower().split()
        tags.extend([word.capitalize() for word in topic_words if len(word) > 3])

        # Common content tags based on keywords
        keyword_tags = {
            'ai': 'AI',
            'artificial intelligence': 'AI',
            'machine learning': 'ML',
            'technology': 'Tech',
            'business': 'Business',
            'marketing': 'Marketing',
            'social media': 'Social Media',
            'content': 'Content',
            'strategy': 'Strategy',
            'tips': 'Tips',
            'guide': 'Guide',
            'tutorial': 'Tutorial'
        }

        content_lower = content.lower()
        for keyword, tag in keyword_tags.items():
            if keyword in content_lower and tag not in tags:
                tags.append(tag)

        return tags[:5]  # Limit to 5 tags
    
    def generate_and_save_content(self,
                                topic: str,
                                content_type: str = "blog",
                                ai_provider: str = "gemini",
                                tone: str = "professional",
                                length: str = "medium") -> Optional[Dict]:
        """Main method to generate content and save to Notion"""

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            # Step 1: Generate content
            task1 = progress.add_task("Generating content...", total=None)

            prompt = self.create_content_prompt(topic, content_type, tone, length)
            content = self.llm_handler.generate_content(prompt, ai_provider)

            if not content:
                console.print("❌ Failed to generate content", style="red")
                return None

            progress.update(task1, description="Content generated ✅")

            # Step 2: Process content
            task2 = progress.add_task("Processing content...", total=None)

            title = self.extract_title_from_content(content)
            tags = self.extract_tags_from_content(content, topic)

            progress.update(task2, description="Content processed ✅")

            # Step 3: Save to Notion
            task3 = progress.add_task("Saving to Notion...", total=None)

            page_id = self.notion_handler.create_content_page(
                title=title,
                content=content,
                content_type=content_type.capitalize(),
                ai_provider=ai_provider.capitalize(),
                tags=tags,
                status="Draft"
            )

            if not page_id:
                console.print("❌ Failed to save to Notion", style="red")
                return None

            progress.update(task3, description="Saved to Notion ✅")

        # Return result summary
        result = {
            "title": title,
            "content_preview": content[:200] + "...",
            "word_count": len(content.split()),
            "tags": tags,
            "notion_page_id": page_id,
            "ai_provider": ai_provider
        }

        console.print("\n🎉 Content created successfully!", style="green bold")
        console.print(f"📝 Title: {title}")
        console.print(f"📊 Word count: {result['word_count']}")
        console.print(f"🏷️  Tags: {', '.join(tags)}")
        console.print(f"🤖 AI Provider: {ai_provider.capitalize()}")

        return result
    
    def test_all_systems(self):
        """Test all components"""
        console.print("🔧 Testing AI Content Agent...\n", style="blue bold")

        # Test LLM
        console.print("1. Testing LLM providers...")
        test_prompt = "Write a one sentence about AI."

        gemini_result = self.llm_handler.generate_content(test_prompt, "gemini")
        ollama_result = self.llm_handler.generate_content(test_prompt, "ollama")

        console.print(f"   Gemini: {'✅' if gemini_result else '❌'}")
        console.print(f"   Ollama: {'✅' if ollama_result else '❌'}")

        # Test Notion
        console.print("\n2. Testing Notion connection...")
        notion_test = self.notion_handler.test_connection()
        console.print(f"   Notion API: {'✅' if notion_test else '❌'}")

        console.print("\n✅ System test complete!" if (gemini_result or ollama_result) and notion_test else "\n❌ Some systems failed!")