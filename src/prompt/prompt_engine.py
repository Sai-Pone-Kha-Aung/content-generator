from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pydantic import BaseModel
from enum import Enum

class ContentType(Enum):
    BLOG = "blog"
    SOCIAL = "social"
    ARTICLE = "article"
    MARKETING = "marketing"
    EMAIL = "email"
    NEWSLETTER = "newsletter"
    PRODUCT_DESCRIPTION = "product_description"
    CASE_STUDY = "case_study"
    TUTORIAL = "tutorial"
    PRESS_RELEASE = "press_release"

class ToneType(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    CREATIVE = "creative"
    HUMOROUS = "humorous"
    AUTHORITATIVE = "authoritative"
    CONVERSATIONAL = "conversational"

class LengthType(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    EXTRA_LONG = "extra_long"

class ContentRequest(BaseModel):
    topic: str
    content_type: ContentType
    tone: ToneType
    length: LengthType
    target_audience: Optional[str] = None
    keywords: Optional[List[str]] = None
    call_to_action: Optional[str] = None
    brand_voice: Optional[str] = None
    custom_instructions: Optional[str] = None
    include_examples: bool = False
    seo_focused: bool = False
    industry: Optional[str] = None

class PromptEngine:
    def __init__(self):
        self.base_prompts = self._load_base_prompts()
        self.prompt_modifiers = self._load_prompt_modifiers()
        self.content_structures = self._load_content_structures()
        
    def _load_base_prompts(self) -> Dict[str, str]:
        """Load base prompt templates for each content type"""
        return {
            ContentType.BLOG.value: """
You are an expert content writer specializing in creating engaging blog posts. 

Write a {length_description} blog post about "{topic}".

REQUIREMENTS:
- Tone: {tone}
- Target audience: {target_audience}
- Word count: {word_count_range}
- Include SEO optimization: {seo_requirements}

STRUCTURE:
1. Compelling headline
2. Engaging introduction with hook
3. Main content with clear headings (H2, H3)
4. Actionable insights and practical tips
5. Conclusion with key takeaways
6. Call-to-action: {call_to_action}

WRITING GUIDELINES:
- Use active voice
- Include relevant examples and case studies
- Add bullet points and numbered lists for readability
- Optimize for search engines with natural keyword integration
- Make it scannable with subheadings
- Include transitional phrases for flow

{additional_instructions}
""",

            ContentType.SOCIAL.value: """
You are a social media expert creating engaging content for {platform}.

Create a {tone} social media post about "{topic}".

REQUIREMENTS:
- Platform: {platform}
- Character limit: {character_limit}
- Target audience: {target_audience}
- Include hashtags: {hashtag_requirements}

STRUCTURE:
1. Attention-grabbing opening
2. Main message with value
3. Call-to-action
4. Relevant hashtags

WRITING GUIDELINES:
- Use emojis strategically
- Create thumb-stopping content
- Include social proof if relevant
- Ask engaging questions
- Use trending hashtags appropriately
- Make it shareable

{additional_instructions}
""",

            ContentType.MARKETING.value: """
You are a conversion copywriter creating persuasive marketing content.

Write {length_description} marketing copy for "{topic}".

REQUIREMENTS:
- Tone: {tone}
- Target audience: {target_audience}
- Primary goal: {marketing_goal}
- Call-to-action: {call_to_action}

STRUCTURE:
1. Attention-grabbing headline
2. Problem identification
3. Solution presentation
4. Benefits and features
5. Social proof/testimonials
6. Urgency/scarcity
7. Strong call-to-action

COPYWRITING TECHNIQUES:
- Use AIDA framework (Attention, Interest, Desire, Action)
- Focus on benefits over features
- Address objections proactively
- Use power words and emotional triggers
- Create urgency without being pushy
- Include specific, measurable claims

{additional_instructions}
""",

            ContentType.EMAIL.value: """
You are an email marketing specialist creating high-converting email campaigns.

Write a {length_description} email about "{topic}".

REQUIREMENTS:
- Email type: {email_type}
- Tone: {tone}
- Target audience: {target_audience}
- Primary goal: {email_goal}

STRUCTURE:
1. Compelling subject line
2. Personal greeting
3. Opening hook
4. Main content with value
5. Clear call-to-action
6. Professional signature

EMAIL BEST PRACTICES:
- Write scannable content
- Use conversational tone
- Personalize when possible
- Include single, clear CTA
- Optimize for mobile reading
- Test different subject lines

{additional_instructions}
""",

            ContentType.ARTICLE.value: """
You are a professional journalist and subject matter expert.

Write a comprehensive {length_description} article about "{topic}".

REQUIREMENTS:
- Tone: {tone}
- Target audience: {target_audience}
- Article type: {article_type}
- Research depth: {research_requirements}

STRUCTURE:
1. Informative headline
2. Executive summary/abstract
3. Introduction with thesis
4. Main sections with evidence
5. Analysis and insights
6. Conclusion with implications
7. References/sources

WRITING STANDARDS:
- Use authoritative sources
- Include data and statistics
- Maintain objectivity
- Use proper citations
- Ensure fact accuracy
- Follow journalistic standards

{additional_instructions}
""",

            ContentType.TUTORIAL.value: """
You are an instructional designer creating step-by-step educational content.

Create a comprehensive tutorial on "{topic}".

REQUIREMENTS:
- Skill level: {skill_level}
- Learning objectives: {learning_objectives}
- Time to complete: {estimated_time}
- Tools/resources needed: {required_tools}

STRUCTURE:
1. Clear title and overview
2. Prerequisites and requirements
3. Learning objectives
4. Step-by-step instructions
5. Screenshots/examples (descriptions)
6. Troubleshooting section
7. Next steps/further learning

INSTRUCTIONAL DESIGN:
- Use clear, actionable language
- Break complex tasks into simple steps
- Include checkpoints and validation
- Anticipate common mistakes
- Provide alternative approaches
- End with practice exercises

{additional_instructions}
"""
        }
    
    def _load_prompt_modifiers(self) -> Dict[str, Dict[str, str]]:
        """Load prompt modifiers for different aspects"""
        return {
            "tone_modifiers": {
                ToneType.PROFESSIONAL.value: "Maintain a professional, authoritative voice with industry-appropriate language.",
                ToneType.CASUAL.value: "Use a relaxed, conversational tone that feels like talking to a friend.",
                ToneType.FRIENDLY.value: "Be warm, approachable, and encouraging in your communication style.",
                ToneType.FORMAL.value: "Use formal language structure with proper grammar and academic tone.",
                ToneType.CREATIVE.value: "Be imaginative, use creative metaphors, and think outside the box.",
                ToneType.HUMOROUS.value: "Include appropriate humor, wit, and light-hearted elements.",
                ToneType.AUTHORITATIVE.value: "Demonstrate expertise, confidence, and thought leadership.",
                ToneType.CONVERSATIONAL.value: "Write as if having a natural conversation with the reader."
            },
            
            "length_modifiers": {
                LengthType.SHORT.value: {
                    "description": "concise and focused",
                    "blog": "300-500 words",
                    "social": "50-100 words",
                    "marketing": "150-300 words",
                    "email": "100-200 words",
                    "article": "400-600 words"
                },
                LengthType.MEDIUM.value: {
                    "description": "well-developed",
                    "blog": "800-1200 words",
                    "social": "100-200 words", 
                    "marketing": "300-500 words",
                    "email": "200-400 words",
                    "article": "800-1200 words"
                },
                LengthType.LONG.value: {
                    "description": "comprehensive and detailed",
                    "blog": "1500-2500 words",
                    "social": "200-300 words",
                    "marketing": "500-1000 words",
                    "email": "400-800 words",
                    "article": "1500-3000 words"
                }
            },
            
            "audience_modifiers": {
                "beginners": "Explain concepts clearly, avoid jargon, include definitions for technical terms.",
                "professionals": "Use industry terminology, assume baseline knowledge, focus on advanced insights.",
                "executives": "Be concise, focus on strategic implications, include ROI and business impact.",
                "technical": "Include technical details, code examples, and implementation specifics.",
                "general": "Use accessible language for a broad audience, explain technical concepts simply."
            },
            
            "seo_modifiers": {
                "high": "Optimize heavily for SEO with keyword density 1-2%, include meta descriptions, use semantic keywords.",
                "medium": "Include target keywords naturally, use related terms, optimize headings for search.",
                "low": "Focus on readability first, include keywords naturally without forcing them.",
                "none": "Write purely for human readers without SEO considerations."
            }
        }
    
    def _load_content_structures(self) -> Dict[str, List[str]]:
        """Load content structure templates"""
        return {
            "blog_structures": {
                "listicle": [
                    "Compelling headline with number",
                    "Brief introduction explaining the value",
                    "Numbered list items with detailed explanations",
                    "Conclusion summarizing key points",
                    "Call-to-action"
                ],
                "how_to": [
                    "Problem statement",
                    "Overview of solution",
                    "Step-by-step instructions",
                    "Tips and best practices",
                    "Common mistakes to avoid",
                    "Conclusion with next steps"
                ],
                "comparison": [
                    "Introduction to options being compared",
                    "Criteria for comparison",
                    "Detailed comparison sections",
                    "Pros and cons analysis",
                    "Recommendation",
                    "Call-to-action"
                ]
            },
            
            "marketing_frameworks": {
                "aida": ["Attention", "Interest", "Desire", "Action"],
                "pas": ["Problem", "Agitation", "Solution"],
                "before_after_bridge": ["Before (current state)", "After (desired state)", "Bridge (solution)"],
                "features_advantages_benefits": ["Features", "Advantages", "Benefits", "Proof"]
            }
        }
    
    def create_enhanced_prompt(self, request: ContentRequest) -> str:
        """Create an enhanced prompt based on the request"""
        
        # Get base prompt template
        base_prompt = self.base_prompts.get(request.content_type.value, "")
        
        # Get modifiers
        tone_modifier = self.prompt_modifiers["tone_modifiers"].get(request.tone.value, "")
        length_info = self.prompt_modifiers["length_modifiers"].get(request.length.value, {})
        
        # Build word count range
        word_count_range = length_info.get(request.content_type.value, "500-800 words")
        length_description = length_info.get("description", "well-developed")
        
        # Build audience targeting
        audience_guidance = ""
        if request.target_audience:
            audience_key = self._categorize_audience(request.target_audience)
            audience_guidance = self.prompt_modifiers["audience_modifiers"].get(audience_key, "")
        
        # Build SEO requirements
        seo_level = "medium" if request.seo_focused else "low"
        seo_requirements = self.prompt_modifiers["seo_modifiers"].get(seo_level, "")
        
        # Build keyword integration
        keyword_guidance = ""
        if request.keywords:
            keyword_guidance = f"\nKEYWORDS TO INCLUDE: {', '.join(request.keywords)}\nIntegrate these keywords naturally throughout the content."
        
        # Build additional instructions
        additional_instructions = []
        
        if request.brand_voice:
            additional_instructions.append(f"BRAND VOICE: {request.brand_voice}")
        
        if request.industry:
            additional_instructions.append(f"INDUSTRY CONTEXT: Tailor content for the {request.industry} industry.")
        
        if request.include_examples:
            additional_instructions.append("Include relevant real-world examples and case studies.")
        
        if request.custom_instructions:
            additional_instructions.append(f"CUSTOM REQUIREMENTS: {request.custom_instructions}")
        
        # Format the prompt
        formatted_prompt = base_prompt.format(
            topic=request.topic,
            tone=request.tone.value,
            length_description=length_description,
            word_count_range=word_count_range,
            target_audience=request.target_audience or "general audience",
            seo_requirements=seo_requirements,
            call_to_action=request.call_to_action or "Engage with this content",
            additional_instructions="\n".join(additional_instructions) if additional_instructions else "",
            # Platform-specific
            platform=getattr(request, 'platform', 'general social media'),
            character_limit=getattr(request, 'character_limit', '280 characters'),
            hashtag_requirements=getattr(request, 'hashtag_requirements', 'Include 3-5 relevant hashtags'),
            # Marketing-specific
            marketing_goal=getattr(request, 'marketing_goal', 'generate leads'),
            # Email-specific
            email_type=getattr(request, 'email_type', 'newsletter'),
            email_goal=getattr(request, 'email_goal', 'inform and engage'),
            # Article-specific
            article_type=getattr(request, 'article_type', 'informational'),
            research_requirements=getattr(request, 'research_requirements', 'well-researched'),
            # Tutorial-specific
            skill_level=getattr(request, 'skill_level', 'beginner'),
            learning_objectives=getattr(request, 'learning_objectives', 'understand the topic'),
            estimated_time=getattr(request, 'estimated_time', '15 minutes'),
            required_tools=getattr(request, 'required_tools', 'none')
        )
        
        # Add keyword guidance
        if keyword_guidance:
            formatted_prompt += keyword_guidance
        
        # Add final enhancement
        formatted_prompt += self._add_quality_guidelines()
        
        return formatted_prompt
    
    def _categorize_audience(self, audience: str) -> str:
        """Categorize audience for appropriate modifier"""
        audience_lower = audience.lower()
        
        if any(word in audience_lower for word in ['beginner', 'new', 'starter', 'novice']):
            return 'beginners'
        elif any(word in audience_lower for word in ['professional', 'expert', 'specialist', 'practitioner']):
            return 'professionals'
        elif any(word in audience_lower for word in ['executive', 'manager', 'leader', 'director', 'ceo']):
            return 'executives'
        elif any(word in audience_lower for word in ['developer', 'engineer', 'technical', 'programmer']):
            return 'technical'
        else:
            return 'general'
    
    def _add_quality_guidelines(self) -> str:
        """Add general quality guidelines to all prompts"""
        return """

QUALITY STANDARDS:
- Ensure accuracy and fact-check claims
- Use clear, concise language
- Maintain consistent voice throughout
- Include transitions between sections
- End with clear next steps
- Proofread for grammar and spelling
- Make content valuable and actionable

OUTPUT FORMAT:
- Provide clean, formatted text
- Use markdown for structure where appropriate
- Include suggested title options
- Separate meta information (suggested tags, SEO title, etc.)
"""

    def get_content_suggestions(self, topic: str, content_type: ContentType) -> Dict[str, List[str]]:
        """Get content suggestions based on topic and type"""
        suggestions = {
            "title_options": self._generate_title_suggestions(topic, content_type),
            "keyword_suggestions": self._generate_keyword_suggestions(topic),
            "structure_options": self._get_structure_suggestions(content_type),
            "cta_suggestions": self._generate_cta_suggestions(content_type)
        }
        return suggestions
    
    def _generate_title_suggestions(self, topic: str, content_type: ContentType) -> List[str]:
        """Generate title suggestions"""
        base_titles = {
            ContentType.BLOG: [
                f"The Complete Guide to {topic}",
                f"Everything You Need to Know About {topic}",
                f"Mastering {topic}: A Step-by-Step Guide",
                f"The Ultimate {topic} Strategy for 2024",
                f"How to Excel at {topic} (Even as a Beginner)"
            ],
            ContentType.SOCIAL: [
                f"Quick tip about {topic} 💡",
                f"The truth about {topic} that nobody talks about",
                f"Why {topic} matters more than you think",
                f"Hot take on {topic} 🔥",
                f"The {topic} game-changer you need to know"
            ],
            ContentType.MARKETING: [
                f"Transform Your Business with {topic}",
                f"Unlock the Power of {topic}",
                f"Why {topic} is Your Secret Weapon",
                f"The {topic} Solution You've Been Looking For",
                f"Get Results Fast with {topic}"
            ]
        }
        return base_titles.get(content_type, [f"Understanding {topic}"])
    
    def _generate_keyword_suggestions(self, topic: str) -> List[str]:
        """Generate keyword suggestions based on topic"""
        # This is a simplified version - in production you might use keyword research APIs
        words = topic.lower().split()
        keywords = words.copy()
        
        # Add common variations
        for word in words:
            keywords.extend([
                f"{word} guide",
                f"{word} tips",
                f"{word} strategy",
                f"{word} best practices",
                f"how to {word}"
            ])
        
        return keywords[:10]  # Return top 10
    
    def _get_structure_suggestions(self, content_type: ContentType) -> List[str]:
        """Get structure suggestions for content type"""
        return list(self.content_structures.get(f"{content_type.value}_structures", {}).keys())
    
    def _generate_cta_suggestions(self, content_type: ContentType) -> List[str]:
        """Generate call-to-action suggestions"""
        ctas = {
            ContentType.BLOG: [
                "What's your experience with this topic? Share in the comments!",
                "Ready to get started? Download our free guide.",
                "Found this helpful? Share it with your network!",
                "Want more tips like this? Subscribe to our newsletter.",
                "Have questions? Contact our team for personalized advice."
            ],
            ContentType.SOCIAL: [
                "Double-tap if you agree! 👍",
                "Save this post for later 📌",
                "Tag someone who needs to see this!",
                "What do you think? Comment below! 👇",
                "Follow for more tips like this! ✨"
            ],
            ContentType.MARKETING: [
                "Get started with a free consultation today!",
                "Claim your limited-time offer now!",
                "Join thousands of satisfied customers!",
                "Don't wait - secure your spot today!",
                "Experience the difference for yourself!"
            ]
        }
        return ctas.get(content_type, ["Take action today!"])