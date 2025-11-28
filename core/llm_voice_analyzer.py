"""
LLM-Based Voice Analyzer

This module uses sophisticated prompts (from prompts/voice_analysis_prompts.py)
to perform deep voice analysis via LLM calls. This complements the rule-based
StyleAnalyzer with more nuanced, human-like analysis.
"""

import os
from typing import Dict, List, Optional, Any
import json

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    OpenAI = None
    Anthropic = None

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from prompts.voice_analysis_prompts import (
        PERSONAL_BRAND_VOICE_GUIDE_PROMPT,
        VOICE_CONNOISSEUR_PROMPT,
        AI_TEXT_HUMANIZER_PROMPT_TEMPLATE,
        VOICE_AVATAR_ALIGNMENT_PROMPT,
        SPEAKER_DETECTION_PROMPT,
        AI_ISM_MASTER_LIST
    )
except ImportError:
    # Fallback if prompts module not found
    PERSONAL_BRAND_VOICE_GUIDE_PROMPT = ""
    VOICE_CONNOISSEUR_PROMPT = ""
    AI_TEXT_HUMANIZER_PROMPT_TEMPLATE = ""
    VOICE_AVATAR_ALIGNMENT_PROMPT = ""
    SPEAKER_DETECTION_PROMPT = ""
    AI_ISM_MASTER_LIST = ""


class LLMVoiceAnalyzer:
    """
    Uses LLM prompts for sophisticated voice analysis.
    This provides deeper, more nuanced analysis than rule-based methods.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        default_model: str = "gpt-4-turbo-preview"
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        # Use Claude 4.5 Haiku for writing, GPT-4o for analysis
        self.default_model = default_model or "claude-haiku-4-5-20251001"
        
        if OpenAI and self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        if Anthropic and self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        else:
            self.anthropic_client = None
    
    def create_personal_brand_voice_guide(
        self,
        writing_samples: List[str],
        author_name: str,
        avatar_blueprint: Optional[Dict] = None,
        voice_connoisseur_analysis: Optional[Dict] = None,
        brand_context: Optional[Dict] = None,
        model: Optional[str] = None
    ) -> Dict:
        """
        Create comprehensive Personal & Brand Voice Guide using the sophisticated prompt.
        
        Args:
            writing_samples: List of text samples (articles, posts, transcripts, etc.)
            author_name: Name of the author
            avatar_blueprint: Optional avatar blueprint document
            voice_connoisseur_analysis: Optional Voice Connoisseur output
            brand_context: Optional brand materials (website, about page, etc.)
            model: AI model to use
            
        Returns:
            Complete voice guide dictionary
        """
        model = model or self.default_model
        
        # Build the prompt with all inputs
        prompt = PERSONAL_BRAND_VOICE_GUIDE_PROMPT + "\n\n"
        
        prompt += f"<input_requirements>\n"
        prompt += f"**Writing & Communication Samples:**\n"
        for i, sample in enumerate(writing_samples, 1):
            prompt += f"\n**Sample {i}:**\n{sample}\n"
        
        if avatar_blueprint:
            prompt += f"\n**Avatar Blueprint:**\n{json.dumps(avatar_blueprint, indent=2)}\n"
        
        if voice_connoisseur_analysis:
            prompt += f"\n**Voice Connoisseur Analysis:**\n{json.dumps(voice_connoisseur_analysis, indent=2)}\n"
        
        if brand_context:
            prompt += f"\n**Brand Context:**\n{json.dumps(brand_context, indent=2)}\n"
        
        prompt += "</input_requirements>\n\n"
        prompt += "Please analyze these samples and create the complete Personal & Brand Voice Guide following the output structure."
        
        # Generate via LLM
        if "gpt" in model.lower():
            response = self._call_openai(prompt, model)
        elif "claude" in model.lower():
            response = self._call_anthropic(prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        # Parse response (assuming structured output)
        # In practice, you'd parse the markdown/structured response
        return {
            "author_name": author_name,
            "analysis": response,
            "samples_analyzed": len(writing_samples),
            "model_used": model
        }
    
    def discover_voice_through_heroes(
        self,
        transcript: str,
        model: Optional[str] = None
    ) -> Dict:
        """
        Use Voice Connoisseur prompt to discover voice through admired writers.
        
        Args:
            transcript: User's stream-of-consciousness about writers they admire
            model: AI model to use
            
        Returns:
            Three artifacts: patterns, hidden insights, voice guide
        """
        model = model or self.default_model
        
        prompt = VOICE_CONNOISSEUR_PROMPT + "\n\n"
        prompt += f"<user_transcript>\n{transcript}\n</user_transcript>\n\n"
        prompt += "Please analyze this transcript and generate all three artifacts."
        
        if "gpt" in model.lower():
            response = self._call_openai(prompt, model)
        elif "claude" in model.lower():
            response = self._call_anthropic(prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        return {
            "analysis": response,
            "model_used": model
        }
    
    def create_ai_humanizer_prompt(
        self,
        voice_guide: Dict,
        avatar_blueprint: Dict,
        author_name: str
    ) -> str:
        """
        Generate personalized AI Text Humanizer prompt for the user.
        
        Args:
            voice_guide: Complete voice guide (from create_personal_brand_voice_guide)
            avatar_blueprint: Avatar blueprint document
            author_name: Name of the author
            
        Returns:
            Complete, ready-to-use humanizer prompt
        """
        # Extract voice identity section from voice guide
        voice_identity = self._extract_voice_identity_section(voice_guide, avatar_blueprint, author_name)
        
        # Build the prompt
        prompt = AI_TEXT_HUMANIZER_PROMPT_TEMPLATE.format(
            name=author_name,
            voice_identity_section=voice_identity,
            ai_ism_master_list=AI_ISM_MASTER_LIST
        )
        
        return prompt
    
    def find_voice_avatar_friction(
        self,
        voice_guide: Dict,
        avatar_blueprint: Dict,
        model: Optional[str] = None
    ) -> Dict:
        """
        Use Voice-Avatar Alignment Optimizer to find friction points.
        
        Args:
            voice_guide: Complete voice guide
            avatar_blueprint: Avatar blueprint
            model: AI model to use
            
        Returns:
            Friction analysis with adjustment rules
        """
        model = model or self.default_model
        
        prompt = VOICE_AVATAR_ALIGNMENT_PROMPT + "\n\n"
        prompt += f"<voice_guide>\n{json.dumps(voice_guide, indent=2)}\n</voice_guide>\n\n"
        prompt += f"<avatar_blueprint>\n{json.dumps(avatar_blueprint, indent=2)}\n</avatar_blueprint>\n\n"
        prompt += "Please analyze for friction points and create the adjustment guide."
        
        if "gpt" in model.lower():
            response = self._call_openai(prompt, model)
        elif "claude" in model.lower():
            response = self._call_anthropic(prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        return {
            "friction_analysis": response,
            "model_used": model
        }
    
    def detect_speakers_and_create_voice_pack(
        self,
        transcripts: List[str],
        model: Optional[str] = None
    ) -> Dict:
        """
        Detect speakers in transcripts and create voice pack for selected speaker.
        
        Args:
            transcripts: List of transcript texts
            model: AI model to use
            
        Returns:
            Speaker detection results and voice pack (after confirmation)
        """
        model = model or self.default_model
        
        combined_transcripts = "\n\n---\n\n".join(transcripts)
        
        prompt = SPEAKER_DETECTION_PROMPT + "\n\n"
        prompt += f"<transcripts>\n{combined_transcripts}\n</transcripts>\n\n"
        prompt += "Please detect all speakers and present findings."
        
        if "gpt" in model.lower():
            response = self._call_openai(prompt, model)
        elif "claude" in model.lower():
            response = self._call_anthropic(prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        return {
            "speaker_detection": response,
            "model_used": model
        }
    
    def _extract_voice_identity_section(
        self,
        voice_guide: Dict,
        avatar_blueprint: Dict,
        author_name: str
    ) -> str:
        """Extract and format voice identity section for humanizer prompt."""
        
        # Extract from voice guide (could be dict or string)
        analysis_text = ""
        if isinstance(voice_guide, dict):
            analysis_text = voice_guide.get("analysis", "")
        elif isinstance(voice_guide, str):
            analysis_text = voice_guide
        
        # Extract audience info from avatar blueprint
        audience_segment = ""
        psychographics = []
        if isinstance(avatar_blueprint, dict):
            strategic = avatar_blueprint.get("strategic_positioning", {})
            audience_segment = strategic.get("broader_audience_segment", "")
            
            psychos = avatar_blueprint.get("psychographics", {})
            values = psychos.get("values", [])
            mindsets = psychos.get("mindsets", [])
            psychographics = values + mindsets
        
        # Build voice identity section
        identity = f"""### Who I Am
{author_name} - Creator of Signal>Noise newsletter, focused on using AI to reveal hidden patterns that make human expertise valuable and irreplaceable. Deeply analytical and reflective writer who uses metaphor and analogy to convey complex insights.

### Who I Write For

**My Audience Segment:**
{audience_segment if audience_segment else "Established experts and ambitious professionals navigating AI adoption--specifically those who value research-backed frameworks, want to create depth without becoming content machines, and seek strategic AI integration that maintains authentic voice."}

**What Defines Them:**
"""
        
        for item in psychographics[:4]:
            identity += f"- {item}\n"
        
        identity += f"""
**How I Position Myself to Them:**
Signal>Noise serves as a bridge between technology and human creativity, positioning as a curator of deep insights focused on the hidden value of human expertise in a tech-driven world.

**What They Respond To:**
- Deep analysis with clear explanations
- Metaphors and analogies that clarify complex ideas
- Conversational tone that invites exploration
- Stories and historical context
- Humility and learner's mindset

**What They Resist:**
- Generic influencer advice
- Surface-level tips without depth
- Overly technical jargon without explanation
- Authoritative tone that talks down
- Formulaic content patterns

### My Voice DNA

**Core Tone:** Curious and reflective, inviting exploration rather than dictating conclusions. Conversational tone that disarms and engages, positioning self as a fellow traveler in the quest for knowledge.

**Language Style:** Rich and varied vocabulary that carries depth and multiple meanings. Prefers terms that resonate on an emotional level, even when discussing technical topics. Comfortable navigating contradictions to highlight depth and nuance.

**Sentence Patterns:** Mixes longer, complex sentences with shorter, impactful statements to maintain rhythm and engagement. Frequent use of first-person plural ("we," "us") to create a sense of community and shared discovery.

**Signature Moves:**
- Employs analogies and metaphors extensively to bridge complex concepts with relatable experiences
- Uses rhetorical questions that challenge readers to think deeply
- Leverages storytelling and historical context to ground abstract concepts
- Demonstrates humility and a learner's mindset
- Utilizes dashes and parentheses to add asides or deepen insights

**Vocabulary Preferences:** Rich, emotionally resonant vocabulary. Prefers words that carry depth and multiple meanings. Avoids overcomplicating to the point of obscurity or relying too heavily on technical jargon without explanation.

### What I NEVER Do

- Overcomplicate to the point of obscurity
- Rely too heavily on technical jargon without explanation
- Use jargon without clarification
- Let complex sentences detract from clarity
- Assume prior knowledge without providing context
- Close off avenues of inquiry prematurely
- Use generic influencer advice or surface-level tips
- Talk down to readers with overly authoritative tone

### My Content Topics

- AI integration and human expertise
- Hidden patterns in professional success
- Strategic thinking and pattern recognition
- Content creation and authentic voice
- Technology and creativity intersection
- Research-backed frameworks and methodologies
- Community of thoughtful practitioners
- Sustainable systems for professionals
"""
        
        return identity
    
    def _call_openai(self, prompt: str, model: str) -> str:
        """Call OpenAI API."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Adjust max_tokens based on model
        # GPT-4 Turbo supports up to 4096 completion tokens
        # GPT-4o supports up to 16384 completion tokens
        if "gpt-4o" in model.lower():
            max_tokens = 8000
        elif "gpt-4-turbo" in model.lower() or "gpt-4-0125" in model.lower():
            max_tokens = 4096
        else:
            max_tokens = 4096  # Safe default
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert voice analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str, model: str) -> str:
        """Call Anthropic API."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        message = self.anthropic_client.messages.create(
            model=model,
            max_tokens=8000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

