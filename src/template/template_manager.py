from typing import Dict, List, Optional
import json
from pathlib import Path
from src.prompt.prompt_engine import ContentType, ToneType, LengthType

class TemplateManager:
    def __init__(self):
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.custom_templates = self._load_custom_templates()
    
    def _load_custom_templates(self) -> Dict:
        """Load custom templates from JSON files"""
        templates = {}
        for file_path in self.templates_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    template_data = json.load(f)
                    templates[file_path.stem] = template_data
            except Exception as e:
                print(f"Error loading template {file_path}: {e}")
        return templates
    
    def save_template(self, name: str, template_data: Dict):
        """Save a custom template"""
        file_path = self.templates_dir / f"{name}.json"
        with open(file_path, 'w') as f:
            json.dump(template_data, f, indent=2)
        self.custom_templates[name] = template_data
    
    def get_industry_templates(self) -> Dict[str, Dict]:
        """Get industry-specific templates"""
        return {
            "technology": {
                "keywords": ["innovation", "digital transformation", "automation", "AI", "machine learning"],
                "tone_preferences": [ToneType.PROFESSIONAL, ToneType.AUTHORITATIVE],
                "common_topics": ["software development", "cybersecurity", "cloud computing", "data analytics"],
                "audience_segments": ["developers", "IT professionals", "tech executives", "early adopters"]
            },
            
            "healthcare": {
                "keywords": ["patient care", "medical research", "healthcare technology", "wellness", "treatment"],
                "tone_preferences": [ToneType.PROFESSIONAL, ToneType.AUTHORITATIVE, ToneType.FRIENDLY],
                "common_topics": ["patient outcomes", "medical devices", "healthcare policy", "preventive care"],
                "audience_segments": ["healthcare professionals", "patients", "medical researchers", "administrators"]
            },
            
            "finance": {
                "keywords": ["investment", "financial planning", "risk management", "returns", "portfolio"],
                "tone_preferences": [ToneType.PROFESSIONAL, ToneType.FORMAL, ToneType.AUTHORITATIVE],
                "common_topics": ["market analysis", "investment strategies", "financial planning", "regulatory compliance"],
                "audience_segments": ["investors", "financial advisors", "business owners", "individuals"]
            },
            
            "education": {
                "keywords": ["learning", "education", "skills development", "training", "knowledge"],
                "tone_preferences": [ToneType.FRIENDLY, ToneType.CONVERSATIONAL, ToneType.PROFESSIONAL],
                "common_topics": ["online learning", "skill development", "educational technology", "career advancement"],
                "audience_segments": ["students", "educators", "professionals", "lifelong learners"]
            },
            
            "marketing": {
                "keywords": ["brand awareness", "customer engagement", "conversion", "ROI", "digital marketing"],
                "tone_preferences": [ToneType.CREATIVE, ToneType.CONVERSATIONAL, ToneType.PROFESSIONAL],
                "common_topics": ["content marketing", "social media", "SEO", "email marketing", "analytics"],
                "audience_segments": ["marketers", "business owners", "agencies", "entrepreneurs"]
            }
        }
    
    def get_seasonal_templates(self) -> Dict[str, Dict]:
        """Get seasonal content templates"""
        return {
            "new_year": {
                "themes": ["resolutions", "fresh start", "goal setting", "planning", "reflection"],
                "angles": ["year-end review", "predictions", "planning guides", "resolution tips"],
                "emotional_triggers": ["motivation", "optimism", "determination", "reflection"]
            },
            
            "spring": {
                "themes": ["renewal", "growth", "fresh beginnings", "cleaning", "optimization"],
                "angles": ["spring cleaning", "new beginnings", "growth strategies", "refreshing approaches"],
                "emotional_triggers": ["energy", "renewal", "hope", "activity"]
            },
            
            "back_to_school": {
                "themes": ["learning", "preparation", "organization", "skill building", "knowledge"],
                "angles": ["learning resources", "skill development", "productivity tips", "educational content"],
                "emotional_triggers": ["curiosity", "preparation", "ambition", "growth"]
            },
            
            "holiday_season": {
                "themes": ["gratitude", "giving", "reflection", "celebration", "community"],
                "angles": ["year-end summaries", "gift guides", "reflection pieces", "gratitude content"],
                "emotional_triggers": ["warmth", "gratitude", "generosity", "reflection"]
            }
        }
    
    def get_viral_content_patterns(self) -> Dict[str, Dict]:
        """Get patterns for viral content"""
        return {
            "listicles": {
                "structure": "numbered list format",
                "optimal_numbers": [5, 7, 10, 15, 21],
                "hooks": ["X things", "X secrets", "X mistakes", "X ways"],
                "engagement_triggers": ["curiosity gaps", "practical value", "easy consumption"]
            },
            
            "how_to_guides": {
                "structure": "step-by-step instructions",
                "hooks": ["How to", "The ultimate guide to", "Master X in Y steps"],
                "engagement_triggers": ["problem-solving", "skill building", "immediate value"]
            },
            
            "contrarian_takes": {
                "structure": "challenge common beliefs",
                "hooks": ["Why X is wrong", "The truth about X", "What nobody tells you about X"],
                "engagement_triggers": ["curiosity", "controversy", "insider knowledge"]
            },
            
            "behind_the_scenes": {
                "structure": "insider perspective",
                "hooks": ["Inside look at", "What really happens", "Behind the scenes of"],
                "engagement_triggers": ["exclusivity", "authenticity", "human connection"]
            }
        }

# Create template files
def create_default_templates():
    """Create default template files"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Blog post template
    blog_template = {
        "name": "Professional Blog Post",
        "content_type": "blog",
        "structure": [
            "Compelling headline with benefit",
            "Hook that addresses reader's pain point",
            "Brief overview of what they'll learn",
            "Main content with subheadings",
            "Actionable takeaways",
            "Conclusion with next steps",
            "Clear call-to-action"
        ],
        "best_practices": [
            "Use H2 and H3 headings for structure",
            "Include bullet points for readability",
            "Add examples and case studies",
            "Optimize for featured snippets",
            "Include internal and external links"
        ],
        "word_count_ranges": {
            "short": "500-800",
            "medium": "1000-1500", 
            "long": "2000-3000"
        }
    }
    
    with open(templates_dir / "blog_template.json", "w") as f:
        json.dump(blog_template, f, indent=2)
    
    # Social media template
    social_template = {
        "name": "Engaging Social Media Post",
        "content_type": "social",
        "platforms": {
            "twitter": {"character_limit": 280, "hashtag_limit": 2},
            "linkedin": {"character_limit": 3000, "hashtag_limit": 5},
            "facebook": {"character_limit": 2000, "hashtag_limit": 3},
            "instagram": {"character_limit": 2200, "hashtag_limit": 10}
        },
        "structure": [
            "Attention-grabbing opening",
            "Value-driven main content",
            "Call-to-action",
            "Relevant hashtags"
        ],
        "engagement_tactics": [
            "Ask questions",
            "Use emojis strategically",
            "Include statistics or facts",
            "Share personal experiences",
            "Create urgency or FOMO"
        ]
    }
    
    with open(templates_dir / "social_template.json", "w") as f:
        json.dump(social_template, f, indent=2)

if __name__ == "__main__":
    create_default_templates()