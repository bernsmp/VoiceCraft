"""
AI Text Humanizer - Built into VoiceCraft

Uses your personalized humanizer prompt to clean AI-generated text
while maintaining your authentic voice.
"""

import os
from typing import Optional
from pathlib import Path

try:
    from openai import OpenAI
    from anthropic import Anthropic
except ImportError:
    OpenAI = None
    Anthropic = None

from .llm_voice_analyzer import LLMVoiceAnalyzer


class Humanizer:
    """Humanize AI-generated text using personalized voice profile"""
    
    def __init__(
        self,
        profile_name: str,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.profile_name = profile_name
        self.model = model or "claude-haiku-4-5-20251001"
        
        # Initialize analyzer (which has LLM clients)
        self.analyzer = LLMVoiceAnalyzer(
            openai_api_key=openai_api_key,
            anthropic_api_key=anthropic_api_key,
            default_model=self.model
        )
        
        # Load humanizer prompt
        self.humanizer_prompt = self._load_humanizer_prompt()
    
    def _load_humanizer_prompt(self) -> Optional[str]:
        """Load the humanizer prompt for this profile"""
        prompt_path = Path(f"./data/outputs/{self.profile_name.lower().replace(' ', '-')}-ai-humanizer-prompt.md")
        
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                return f.read()
        
        # If prompt doesn't exist, generate it on the fly
        return None
    
    def humanize(
        self,
        text: str,
        show_analysis: bool = False,
        model: Optional[str] = None
    ) -> dict:
        """
        Humanize AI-generated text.
        
        Args:
            text: AI-generated text to humanize
            show_analysis: If True, return analysis of changes
            model: Override default model
            
        Returns:
            Dictionary with humanized text and optional analysis
        """
        model = model or self.model
        
        # If prompt doesn't exist, generate it first
        if not self.humanizer_prompt:
            print("Generating humanizer prompt...")
            self._generate_prompt()
            self.humanizer_prompt = self._load_humanizer_prompt()
        
        if not self.humanizer_prompt:
            raise ValueError("Could not load or generate humanizer prompt")
        
        # Build complete prompt
        full_prompt = self.humanizer_prompt + "\n\n---\n\n**Text to humanize:**\n\n" + text
        
        # Call LLM
        if "gpt" in model.lower():
            humanized = self.analyzer._call_openai(full_prompt, model)
        elif "claude" in model.lower():
            humanized = self.analyzer._call_anthropic(full_prompt, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        result = {
            "original": text,
            "humanized": humanized,
            "model_used": model
        }
        
        if show_analysis:
            # Get analysis of what changed
            analysis_prompt = f"""
Compare these two versions and tell me what changed:

ORIGINAL:
{text}

HUMANIZED:
{humanized}

What AI-isms were removed? What voice elements were added?
"""
            
            if "gpt" in model.lower():
                analysis = self.analyzer._call_openai(analysis_prompt, model)
            else:
                analysis = self.analyzer._call_anthropic(analysis_prompt, model)
            
            result["analysis"] = analysis
        
        return result
    
    def _generate_prompt(self):
        """Generate humanizer prompt if it doesn't exist"""
        from .voice_profiler import VoiceProfiler
        
        profiler = VoiceProfiler()
        voice_profile = profiler.load_profile(self.profile_name)
        
        if not voice_profile:
            raise ValueError(f"Profile '{self.profile_name}' not found. Create it first.")
        
        # Create avatar blueprint (basic version)
        avatar_blueprint = {
            "strategic_positioning": {
                "broader_audience_segment": "Established experts and ambitious professionals"
            },
            "psychographics": {
                "values": ["Research-backed frameworks", "Authentic voice"],
                "mindsets": ["Depth over volume"]
            }
        }
        
        # Generate prompt
        prompt = self.analyzer.create_ai_humanizer_prompt(
            voice_guide=voice_profile.get("llm_analysis", {}),
            avatar_blueprint=avatar_blueprint,
            author_name=self.profile_name
        )
        
        # Save it
        output_path = Path(f"./data/outputs/{self.profile_name.lower().replace(' ', '-')}-ai-humanizer-prompt.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(prompt)
        
        print(f"✓ Humanizer prompt generated: {output_path}")


# Convenience function
def humanize_text(
    text: str,
    profile_name: str = "Max Bernstein",
    show_analysis: bool = False,
    model: Optional[str] = None
) -> str:
    """
    Quick function to humanize text.
    
    Usage:
        from core.humanizer import humanize_text
        cleaned = humanize_text("AI-generated text here...")
    """
    humanizer = Humanizer(profile_name, model=model)
    result = humanizer.humanize(text, show_analysis=show_analysis)
    return result["humanized"]

