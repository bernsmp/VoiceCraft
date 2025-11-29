"""
Content Generator - Generate content using AI with style fusion

This module handles:
- AI-powered content generation (OpenAI, Anthropic)
- Multi-format output (articles, LinkedIn, Twitter, FAQs)
- Iterative refinement
- Voice consistency verification
"""

import os
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass
import json

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    print("Warning: AI libraries not installed. Install with: pip install openai anthropic")
    OpenAI = None
    Anthropic = None

from .style_blender import StyleBlender
from .voice_profiler import VoiceProfiler

# Import prompt assembler for modular prompts
try:
    from .prompt_assembler import PromptAssembler
    PROMPT_ASSEMBLER_AVAILABLE = True
except ImportError:
    PROMPT_ASSEMBLER_AVAILABLE = False

# Import ELITE Intelligence Unit if available
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from prompts.elite_intelligence_unit import EliteIntelligenceUnit, get_elite_prompt
    ELITE_AVAILABLE = True
except ImportError:
    ELITE_AVAILABLE = False

# Import Knowledge Base
try:
    from .knowledge_base import get_knowledge_base
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_BASE_AVAILABLE = False


ContentFormat = Literal["article", "linkedin", "twitter", "faq", "email"]


@dataclass
class GenerationConfig:
    """Configuration for content generation"""
    format: ContentFormat = "article"
    target_length: int = 1000  # words
    tone: Optional[str] = None
    include_cta: bool = True
    aeo_optimize: bool = True
    temperature: float = 0.7
    max_retries: int = 3
    use_elite_unit: bool = False  # Use ELITE Intelligence Unit prompt system
    use_modular_prompts: bool = True  # Use modular prompt system (Max's voice)
    input_type: str = "topic"  # voice_note, transcript, idea, existing, analytics, comments, topic
    platforms: Optional[List[str]] = None  # List of platforms to optimize for
    use_modular_prompts: bool = True  # Use modular prompt system (Max's voice)
    input_type: str = "topic"  # voice_note, transcript, idea, existing, analytics, comments, topic
    platforms: Optional[List[str]] = None  # List of platforms to optimize for


class ContentGenerator:
    """Generate content with AI using blended styles"""
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        default_model: str = "claude-haiku-4-5-20251001"  # Claude 4.5 Haiku
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.default_model = default_model
        
        # Initialize clients
        if OpenAI and self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        if Anthropic and self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        else:
            self.anthropic_client = None
        
        # Initialize helper classes
        self.blender = StyleBlender()
        self.profiler = VoiceProfiler()
    
    def generate(
        self,
        content_brief: str,
        voice_profile: Dict,
        style_influences: Optional[List[tuple]] = None,
        config: Optional[GenerationConfig] = None,
        model: Optional[str] = None
    ) -> Dict:
        """
        Generate content with blended style
        
        Args:
            content_brief: What to write about
            voice_profile: Base voice profile
            style_influences: List of (style_profile, weight) tuples
            config: Generation configuration
            model: AI model to use (overrides default)
            
        Returns:
            Dictionary with generated content and metadata
        """
        config = config or GenerationConfig()
        model = model or self.default_model
        
        # Blend styles
        if style_influences:
            blended_style = self.blender.blend_styles(
                base_voice=voice_profile,
                influences=style_influences
            )
        else:
            # Use only base voice
            blended_style = {
                "base_voice": voice_profile.get("metadata", {}).get("name", "Unknown"),
                "base_weight": 1.0,
                "influences": [],
                "composite_instructions": f"Write in {voice_profile.get('metadata', {}).get('name', 'this')}'s voice.",
                "blend_summary": voice_profile.get("metadata", {}).get("name", "Base voice")
            }
        
        # Create prompt (prioritize modular prompts, then ELITE, then default)
        if config.use_modular_prompts and PROMPT_ASSEMBLER_AVAILABLE:
            prompt = self._create_modular_prompt(content_brief, config)
        elif config.use_elite_unit and ELITE_AVAILABLE:
            prompt = self._create_elite_prompt(content_brief, voice_profile, config)
        else:
            prompt = self._create_prompt(blended_style, content_brief, config)
        
        # Generate content
        if "gpt" in model.lower() or "o1" in model.lower():
            content = self._generate_openai(prompt, model, config)
        elif "claude" in model.lower():
            content = self._generate_anthropic(prompt, model, config)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        # Verify voice consistency (handle both LLM and rule-based profiles)
        voice_match = {"match_score": 0, "matches_voice": False}
        try:
            profile_name = voice_profile.get("metadata", {}).get("name", "")
            if profile_name:
                # Check if profile has style data (rule-based) or llm_analysis (LLM-based)
                if "style" in voice_profile or "llm_analysis" in voice_profile:
                    voice_match = self.profiler.verify_content(profile_name, content)
        except Exception as e:
            # If verification fails, continue without it
            pass
        
        # Package results
        result = {
            "content": content,
            "metadata": {
                "format": config.format,
                "word_count": len(content.split()),
                "model_used": model,
                "style_blend": blended_style["blend_summary"],
                "voice_match_score": voice_match.get("match_score", 0)
            },
            "voice_verification": voice_match,
            "prompt_used": prompt
        }
        
        return result
    
    def generate_multi_format(
        self,
        content_brief: str,
        voice_profile: Dict,
        formats: List[ContentFormat],
        style_influences: Optional[List[tuple]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Dict]:
        """
        Generate content in multiple formats at once
        
        Returns:
            Dictionary mapping format to generated content
        """
        results = {}
        
        for fmt in formats:
            config = GenerationConfig(format=fmt)
            results[fmt] = self.generate(
                content_brief=content_brief,
                voice_profile=voice_profile,
                style_influences=style_influences,
                config=config,
                model=model
            )
        
        return results
    
    def refine_content(
        self,
        original_content: str,
        refinement_instructions: str,
        voice_profile: Dict,
        model: Optional[str] = None
    ) -> Dict:
        """
        Refine existing content based on instructions
        
        Args:
            original_content: Content to refine
            refinement_instructions: How to improve it
            voice_profile: Voice profile to maintain
            model: AI model to use
            
        Returns:
            Refined content with metadata
        """
        model = model or self.default_model
        
        prompt = f"""Refine the following content based on these instructions:

Instructions: {refinement_instructions}

Maintain the voice and style of: {voice_profile.get('metadata', {}).get('name', 'the author')}

Original Content:
{original_content}

Refined Content:"""
        
        if "gpt" in model.lower():
            refined = self._generate_openai(prompt, model, GenerationConfig())
        else:
            refined = self._generate_anthropic(prompt, model, GenerationConfig())
        
        return {
            "original": original_content,
            "refined": refined,
            "instructions": refinement_instructions
        }
    
    def _create_prompt(
        self,
        blended_style: Dict,
        content_brief: str,
        config: GenerationConfig
    ) -> str:
        """Create the complete generation prompt"""
        # Format-specific instructions
        format_instructions = self._get_format_instructions(config.format, config.target_length)
        
        # AEO optimization instructions
        aeo_instructions = ""
        if config.aeo_optimize:
            # Extract potential keywords from content brief
            keywords = self._extract_keywords_from_brief(content_brief)
            keywords_text = f"\n- Primary keywords: {', '.join(keywords[:5])}" if keywords else ""
            
            aeo_instructions = f"""
## AEO (Answer Engine Optimization) Requirements:
- Use clear, natural language that answers questions directly and comprehensively
- Include relevant entities, concepts, and industry-specific terminology naturally
- Structure content for easy extraction: use lists, clear headings (H2, H3), bullet points, and tables where appropriate
- Provide comprehensive, authoritative information that fully addresses the topic
- Answer the "who, what, when, where, why, and how" questions readers might have
- Include specific examples, case studies, and data points to support claims
- Use natural language patterns that match how people actually search and ask questions
- Ensure content flows logically and builds understanding progressively
{keywords_text}

## Schema Markup Considerations:
- Structure content so it can be easily marked up with schema.org types (Article, FAQPage, HowTo, etc.)
- Use clear question-answer format for FAQs
- Include step-by-step instructions where applicable
- Add structured data hints in headings and lists

## Meta Optimization:
- Create a compelling title tag (50-60 characters) that includes primary keywords naturally
- Write a meta description (150-160 characters) that summarizes the content and includes a call-to-action
- Ensure the headline/title is optimized for both search engines and human readers
"""
        
        # Knowledge base integration
        knowledge_context = ""
        if KNOWLEDGE_BASE_AVAILABLE:
            try:
                kb = get_knowledge_base()
                knowledge_context = kb.format_for_prompt(content_brief, max_frameworks=3, max_cases=2)
                if knowledge_context:
                    knowledge_context = f"\n## Knowledge Base Context:\n{knowledge_context}\n"
            except Exception as e:
                print(f"⚠️  Error loading knowledge base: {e}")
        
        # Build complete prompt
        prompt = f"""{blended_style['composite_instructions']}

## Content Brief:
{content_brief}
{knowledge_context}
## Format:
{format_instructions}

{aeo_instructions}

## Additional Requirements:
- Target length: ~{config.target_length} words
- {f"Tone: {config.tone}" if config.tone else "Maintain authentic voice"}
- {'Include a clear call-to-action' if config.include_cta else 'No hard sell'}
- Ensure the content flows naturally and engages the reader
- Use specific examples and actionable insights where appropriate
- Reference frameworks and case studies from the knowledge base when relevant
- Draw from authentic experience and proven methodologies

Generate the content now:"""
        
        return prompt
    
    def _create_modular_prompt(
        self,
        content_brief: str,
        config: GenerationConfig
    ) -> str:
        """Create prompt using modular prompt system"""
        if not PROMPT_ASSEMBLER_AVAILABLE:
            # Fallback to regular prompt
            blended_style = {
                "composite_instructions": "Write in Max Bernstein's voice."
            }
            return self._create_prompt(blended_style, content_brief, config)
        
        # Build prompt from modular files
        assembler = PromptAssembler()
        prompt = assembler.build_prompt(
            user_input=content_brief,
            input_type=config.input_type,
            platforms=config.platforms or [],
            include_viral=True,
            include_platforms=bool(config.platforms),
            include_multiplication=bool(config.platforms and len(config.platforms) > 1)
        )
        
        # Add knowledge base context
        if KNOWLEDGE_BASE_AVAILABLE:
            try:
                kb = get_knowledge_base()
                knowledge_context = kb.format_for_prompt(content_brief, max_frameworks=3, max_cases=2)
                if knowledge_context:
                    prompt += f"\n\n## Knowledge Base Context:\n{knowledge_context}\n"
                    prompt += "\n## Instructions:\n- Reference frameworks and case studies from the knowledge base when relevant\n- Draw from authentic experience and proven methodologies\n"
            except Exception as e:
                print(f"⚠️  Error loading knowledge base: {e}")
        
        # Add format and length requirements
        format_instructions = self._get_format_instructions(config.format, config.target_length)
        prompt += f"\n\n## Format Requirements:\n{format_instructions}\n\n## Target Length: ~{config.target_length} words\n"
        
        return prompt
    
    def _create_elite_prompt(
        self,
        content_brief: str,
        voice_profile: Dict,
        config: GenerationConfig
    ) -> str:
        """Create prompt using ELITE Intelligence Unit system"""
        if not ELITE_AVAILABLE:
            # Fallback to regular prompt
            return self._create_prompt(
                {"composite_instructions": "Write in the user's voice."},
                content_brief,
                config
            )
        
        # Get ELITE prompt
        elite_unit = EliteIntelligenceUnit()
        return elite_unit.get_content_generation_prompt(
            topic=content_brief,
            output_format=config.format,
            target_length=config.target_length,
            voice_profile=voice_profile
        )
    
    def _extract_keywords_from_brief(self, brief: str) -> List[str]:
        """Extract potential keywords from content brief"""
        # Simple keyword extraction - look for important nouns and phrases
        import re
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'about', 'into', 'through', 'during', 'including', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'to', 'of', 'in', 'for', 'on', 'at', 'by', 'about', 'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', 'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'around', 'down', 'off', 'above', 'near'}
        
        # Extract words (2+ characters, alphanumeric)
        words = re.findall(r'\b[a-zA-Z]{2,}\b', brief.lower())
        
        # Filter stop words and get unique words
        keywords = [w for w in words if w not in stop_words]
        
        # Count frequency and return top keywords
        from collections import Counter
        word_freq = Counter(keywords)
        
        # Return top keywords (most frequent, but prioritize longer words)
        top_keywords = [word for word, count in word_freq.most_common(10)]
        
        # Also extract potential phrases (2-3 word combinations)
        phrases = []
        words_list = brief.lower().split()
        for i in range(len(words_list) - 1):
            phrase = f"{words_list[i]} {words_list[i+1]}"
            if len(phrase) > 5 and not any(sw in phrase for sw in stop_words):
                phrases.append(phrase)
        
        # Combine and return unique keywords/phrases
        all_keywords = list(set(top_keywords + phrases[:5]))
        return all_keywords[:10]
    
    def generate_meta_tags(self, content: str, title: Optional[str] = None) -> Dict[str, str]:
        """
        Generate optimized meta tags (title, description) for SEO
        
        Args:
            content: The content to generate meta tags for
            title: Optional custom title (if not provided, extracted from content)
            
        Returns:
            Dictionary with 'title', 'description', 'keywords'
        """
        # Extract title from content if not provided
        if not title:
            # Look for first H1 or first line
            lines = content.split('\n')
            for line in lines[:10]:  # Check first 10 lines
                line = line.strip()
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    break
                elif line and len(line) < 100 and not line.startswith('#'):
                    title = line.strip()
                    break
            
            if not title:
                # Fallback: use first 60 characters
                title = content[:60].strip()
        
        # Clean title
        title = title.replace('\n', ' ').strip()
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Generate meta description from content
        # Take first 2-3 sentences or first 155 characters
        sentences = content.split('.')
        description = ""
        
        for i, sentence in enumerate(sentences[:3]):
            test_desc = description + sentence.strip() + ". "
            if len(test_desc) <= 160:
                description = test_desc
            else:
                break
        
        if not description:
            description = content[:155].strip()
        
        # Clean description
        description = description.replace('\n', ' ').strip()
        if len(description) > 160:
            description = description[:157] + "..."
        
        # Extract keywords
        keywords = self._extract_keywords_from_brief(content)
        keywords_str = ', '.join(keywords[:5])
        
        return {
            "title": title,
            "description": description,
            "keywords": keywords_str
        }
    
    def suggest_schema_markup(self, content: str, format: ContentFormat = "article") -> Dict[str, Any]:
        """
        Suggest schema.org markup based on content structure
        
        Args:
            content: The content to analyze
            format: Content format (article, faq, etc.)
            
        Returns:
            Dictionary with suggested schema types and properties
        """
        suggestions = {
            "primary_type": "Article",
            "properties": {},
            "additional_types": []
        }
        
        # Detect FAQ structure
        if "?" in content and format == "faq":
            suggestions["primary_type"] = "FAQPage"
            suggestions["properties"]["mainEntity"] = "Array of Question/Answer objects"
        
        # Detect HowTo structure
        if any(word in content.lower() for word in ["step", "how to", "instructions", "process"]):
            suggestions["additional_types"].append("HowTo")
        
        # Detect Article structure
        if format == "article":
            suggestions["primary_type"] = "Article"
            suggestions["properties"]["headline"] = "Extract from H1"
            suggestions["properties"]["articleBody"] = "Full content"
            suggestions["properties"]["author"] = "Louie Bernstein"
        
        return suggestions
    
    def _get_format_instructions(self, format: ContentFormat, target_length: int) -> str:
        """Get format-specific instructions"""
        formats = {
            "article": f"""Write a complete article ({target_length} words) with:
- Compelling headline
- Strong opening hook
- Clear structure with subheadings
- Actionable insights
- Natural conclusion""",
            
            "linkedin": f"""Write a LinkedIn post ({min(target_length, 300)} words max) with:
- Scroll-stopping first line
- Personal insight or story
- Clear value proposition
- Engagement hook (question or call-to-action)
- Appropriate use of line breaks for readability""",
            
            "twitter": f"""Write a Twitter thread ({min(target_length, 280)} characters per tweet) with:
- Hook tweet that stops the scroll
- Clear progression of ideas
- Numbered or structured format
- Strong conclusion with CTA
- Each tweet should stand alone but flow together""",
            
            "faq": f"""Write FAQ-style content with:
- Clear, question-based headings
- Concise, direct answers
- Scannable format
- Cover the most important questions comprehensively""",
            
            "email": f"""Write an email ({min(target_length, 500)} words) with:
- Attention-grabbing subject line
- Personal greeting
- Clear value proposition
- Single, focused message
- Clear call-to-action"""
        }
        
        return formats.get(format, formats["article"])
    
    def _generate_openai(
        self,
        prompt: str,
        model: str,
        config: GenerationConfig
    ) -> str:
        """Generate content using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Check API key.")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who can adapt to any writing style."},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.temperature,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            return content.strip()
        
        except Exception as e:
            raise Exception(f"OpenAI generation failed: {str(e)}")
    
    def _generate_anthropic(
        self,
        prompt: str,
        model: str,
        config: GenerationConfig
    ) -> str:
        """Generate content using Anthropic Claude"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized. Check API key.")
        
        try:
            message = self.anthropic_client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=config.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            return content.strip()
        
        except Exception as e:
            raise Exception(f"Anthropic generation failed: {str(e)}")


# Example usage
if __name__ == "__main__":
    # This would require actual API keys to run
    print("Content Generator module loaded")
    print("Example usage requires OpenAI or Anthropic API keys")
    
    # Mock example
    mock_voice = {
        "metadata": {"name": "Test Author"},
        "style": {}
    }
    
    generator = ContentGenerator()
    print(f"Generator initialized: OpenAI={'✓' if generator.openai_client else '✗'}, Anthropic={'✓' if generator.anthropic_client else '✗'}")

