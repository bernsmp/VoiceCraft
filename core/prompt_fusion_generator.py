"""
Prompt Fusion Generator

Uses your writer prompts as style influences in content generation.
This is the ACTUAL unique feature - blending your voice with master writers.
"""

import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from .prompt_library import get_prompt_library
from .voice_profiler import VoiceProfiler


class PromptFusionGenerator:
    """
    Generate content using your voice + writer prompts as influences
    
    This is the unique feature: Blend your voice with James Clear, Malcolm Gladwell,
    Paul Graham, etc. using their actual writing prompts.
    """
    
    def __init__(
        self,
        profile_name: str,
        anthropic_api_key: Optional[str] = None
    ):
        self.profile_name = profile_name
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if Anthropic and self.anthropic_api_key:
            self.client = Anthropic(api_key=self.anthropic_api_key)
        else:
            self.client = None
        
        self.profiler = VoiceProfiler()
        self.voice_profile = self.profiler.load_profile(profile_name)
        if not self.voice_profile:
            raise ValueError(f"Profile '{profile_name}' not found")
        
        self.prompt_library = get_prompt_library()
    
    def generate_with_prompt_fusion(
        self,
        topic: str,
        writer_influences: List[Tuple[str, float]],  # [("James Clear", 0.3), ("Paul Graham", 0.2)]
        output_format: str = "article",
        target_length: int = 1200,
        model: str = "claude-haiku-4-5-20251001"
    ) -> Dict:
        """
        Generate content blending your voice with writer prompts
        
        Args:
            topic: What to write about
            writer_influences: List of (writer_name, weight) tuples
            output_format: "article", "linkedin", etc.
            target_length: Target word count
            model: Claude model to use
            
        Returns:
            Generated content with fusion details
        """
        
        if not self.client:
            raise ValueError("Anthropic API key not set")
        
        # Build fusion prompt
        fusion_prompt = self._build_fusion_prompt(topic, writer_influences, output_format, target_length)
        
        # Generate
        message = self.client.messages.create(
            model=model,
            max_tokens=4000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": fusion_prompt}
            ]
        )
        
        content = message.content[0].text
        
        return {
            "content": content,
            "topic": topic,
            "fusion": {
                "base_voice": self.profile_name,
                "influences": [
                    {"writer": name, "weight": weight}
                    for name, weight in writer_influences
                ]
            },
            "word_count": len(content.split()),
            "model_used": model
        }
    
    def _build_fusion_prompt(
        self,
        topic: str,
        writer_influences: List[Tuple[str, float]],
        output_format: str,
        target_length: int
    ) -> str:
        """Build complete prompt with voice fusion"""
        
        # Extract voice profile details
        llm_analysis = self.voice_profile.get("llm_analysis", {})
        voice_analysis = llm_analysis.get("analysis", "")
        
        # Build voice description
        voice_desc = f"""## Your Base Voice: {self.profile_name}

Write in {self.profile_name}'s authentic voice. 

"""
        
        # Use the analysis text if available
        if voice_analysis:
            # Extract key parts from the analysis (it's a markdown string)
            voice_desc += f"Voice characteristics:\n{voice_analysis[:1000]}...\n\n"
        else:
            # Fallback description
            voice_desc += """Key characteristics:
- Direct and grounded communication
- Story-driven openings with historical examples
- Conversational "we" and direct "you" address
- Philosophical depth wrapped in accessible stories
- Average sentence length: ~12 words
- Mix of short fragments and longer reflective sentences

"""
        
        # Start building prompt
        prompt = f"""# Content Generation with Style Fusion

{voice_desc}

## Style Influences to Blend In

You will blend {self.profile_name}'s base voice (70%) with the following writer styles:

"""
        
        # Add each writer influence with FULL prompts
        total_weight = sum(weight for _, weight in writer_influences)
        
        for writer_name, weight in writer_influences:
            writer_prompt_data = self.prompt_library.get_prompt(writer_name)
            writer_prompt = writer_prompt_data["prompt"] if writer_prompt_data else None
            
            if writer_prompt:
                influence_pct = int((weight / total_weight) * 100) if total_weight > 0 else 0
                prompt_type = writer_prompt_data.get("type", "general")
                
                prompt += f"""
### {writer_name} ({influence_pct}% influence) - {prompt_type}

{writer_prompt}

**Blending instructions:** Incorporate approximately {influence_pct}% of {writer_name}'s style elements while maintaining {self.profile_name}'s core voice. This means:
- Use {writer_name}'s structural approaches and techniques where appropriate
- Incorporate their voice markers and signature patterns subtly
- Maintain {self.profile_name}'s authentic voice as the foundation (70%)
- The result should feel cohesive, not like a patchwork

"""
        
        # Add generation instructions
        prompt += f"""
## Task

Generate a {output_format} on the topic: "{topic}"

**Requirements:**
- Target length: ~{target_length} words
- Base voice: {self.profile_name} (70% - maintain this as the foundation)
- Style influences: {', '.join([f"{name} ({int(w/total_weight*100)}%)" for name, w in writer_influences])}
- Output format: {output_format}

**The blend should:**
- Sound authentically like {self.profile_name} (this is the base)
- Incorporate stylistic elements from the influenced writers (subtle, not dominant)
- Feel cohesive and natural, not frankensteined
- Maintain {self.profile_name}'s direct, grounded, story-driven style
- Enhance with elements from: {', '.join([f"{name}'s {self.prompt_library.get_prompt(name)['type']}" for name, _ in writer_influences])}

**Important:** The content should read as if {self.profile_name} wrote it, but elevated with techniques from the master writers. The influences should enhance, not replace, the base voice.

Generate the content now:
"""
        
        return prompt


# Convenience function
def generate_with_fusion(
    topic: str,
    profile_name: str = "Max Bernstein",
    writer_influences: List[Tuple[str, float]] = None,
    output_format: str = "article",
    target_length: int = 1200
) -> str:
    """
    Quick function to generate with style fusion
    
    Usage:
        content = generate_with_fusion(
            "How AI is changing expertise",
            writer_influences=[("James Clear", 0.3), ("Paul Graham", 0.2)]
        )
    """
    generator = PromptFusionGenerator(profile_name)
    result = generator.generate_with_prompt_fusion(
        topic=topic,
        writer_influences=writer_influences or [],
        output_format=output_format,
        target_length=target_length
    )
    return result["content"]

