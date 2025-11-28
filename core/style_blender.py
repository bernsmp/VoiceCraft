"""
Style Blender - Combine multiple writing styles with weights

This module handles:
- Blending style profiles with specified weights
- Creating composite style instructions for AI
- Adjusting blend ratios dynamically
"""

from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path


class StyleBlender:
    """Blend multiple writing styles into a composite style"""
    
    def __init__(self, styles_dir: str = "./styles/profiles"):
        self.styles_dir = Path(styles_dir)
        self.styles_dir.mkdir(parents=True, exist_ok=True)
    
    def blend_styles(
        self,
        base_voice: Dict,
        influences: List[Tuple[Dict, float]],
        normalize: bool = True
    ) -> Dict:
        """
        Blend a base voice with style influences
        
        Args:
            base_voice: Base voice profile (60-70% weight usually)
            influences: List of (style_profile, weight) tuples
            normalize: If True, ensure weights sum to 1.0
            
        Returns:
            Blended style profile with instructions
        """
        # Start with base voice at dominant weight
        base_weight = 0.7  # 70% base voice
        
        # Normalize influence weights
        if influences:
            total_influence_weight = sum(weight for _, weight in influences)
            if normalize and total_influence_weight > 0:
                influences = [(style, (weight / total_influence_weight) * (1 - base_weight)) 
                             for style, weight in influences]
        
        # Create blended profile
        blended = {
            "base_voice": base_voice.get("metadata", {}).get("name", "Unknown"),
            "base_weight": base_weight,
            "influences": [
                {
                    "name": style.get("metadata", {}).get("name", "Unknown"),
                    "weight": weight,
                    "style_elements": self._extract_key_elements(style)
                }
                for style, weight in influences
            ],
            "composite_instructions": self._generate_instructions(base_voice, influences),
            "blend_summary": self._create_blend_summary(base_voice, influences)
        }
        
        return blended
    
    def _extract_key_elements(self, style_profile: Dict) -> Dict:
        """Extract the most distinctive elements from a style"""
        style = style_profile.get("style", {})
        
        key_elements = {
            "sentence_structure": {},
            "vocabulary": {},
            "rhetorical_devices": {},
            "emotional_tone": {}
        }
        
        # Sentence structure highlights
        sentence = style.get("sentence_structure", {})
        if sentence.get("avg_sentence_length", 0) < 15:
            key_elements["sentence_structure"]["short_punchy"] = True
        if sentence.get("fragment_ratio", 0) > 0.15:
            key_elements["sentence_structure"]["uses_fragments"] = True
        if sentence.get("question_frequency", 0) > 0.1:
            key_elements["sentence_structure"]["rhetorical_questions"] = True
        
        # Vocabulary highlights
        vocab = style.get("vocabulary", {})
        if vocab.get("reading_ease_score", 0) > 70:
            key_elements["vocabulary"]["simple_language"] = True
        if vocab.get("power_word_density", 0) > 0.01:
            key_elements["vocabulary"]["power_words"] = True
        
        # Rhetorical devices
        rhetoric = style.get("rhetorical_devices", {})
        if rhetoric.get("repetition_for_emphasis", 0) > 0.1:
            key_elements["rhetorical_devices"]["repetition"] = True
        if rhetoric.get("contrast_usage", 0) > 0.1:
            key_elements["rhetorical_devices"]["contrast"] = True
        if rhetoric.get("rule_of_threes", 0) > 0.05:
            key_elements["rhetorical_devices"]["rule_of_threes"] = True
        
        # Emotional tone
        tone = style.get("emotional_tone", {})
        if tone.get("urgency_level", 0) > 0.01:
            key_elements["emotional_tone"]["urgent"] = True
        if tone.get("confidence_level", 0) > 0.01:
            key_elements["emotional_tone"]["confident"] = True
        if tone.get("sentiment_polarity", 0) > 0.3:
            key_elements["emotional_tone"]["positive"] = True
        
        return key_elements
    
    def _generate_instructions(
        self,
        base_voice: Dict,
        influences: List[Tuple[Dict, float]]
    ) -> str:
        """
        Generate natural language instructions for AI content generation
        """
        instructions = []
        
        # Base voice instructions
        base_name = base_voice.get("metadata", {}).get("name", "the author")
        instructions.append(f"Write primarily in {base_name}'s voice and style.")
        
        # Add influence-specific instructions
        for style_profile, weight in influences:
            influence_name = style_profile.get("metadata", {}).get("name", "this writer")
            elements = self._extract_key_elements(style_profile)
            
            style_notes = []
            
            # Sentence structure
            if elements["sentence_structure"].get("short_punchy"):
                style_notes.append("short, punchy sentences")
            if elements["sentence_structure"].get("uses_fragments"):
                style_notes.append("occasional sentence fragments for impact")
            if elements["sentence_structure"].get("rhetorical_questions"):
                style_notes.append("rhetorical questions")
            
            # Vocabulary
            if elements["vocabulary"].get("simple_language"):
                style_notes.append("clear, simple language")
            if elements["vocabulary"].get("power_words"):
                style_notes.append("power words")
            
            # Rhetorical devices
            if elements["rhetorical_devices"].get("repetition"):
                style_notes.append("repetition for emphasis")
            if elements["rhetorical_devices"].get("contrast"):
                style_notes.append("contrast and juxtaposition")
            if elements["rhetorical_devices"].get("rule_of_threes"):
                style_notes.append("rule of three")
            
            # Emotional tone
            if elements["emotional_tone"].get("urgent"):
                style_notes.append("sense of urgency")
            if elements["emotional_tone"].get("confident"):
                style_notes.append("confident assertions")
            
            if style_notes:
                emphasis = "heavily" if weight > 0.25 else "subtly"
                instructions.append(
                    f"Incorporate {emphasis} from {influence_name}: " + 
                    ", ".join(style_notes) + "."
                )
        
        # General guidelines
        instructions.append("Maintain authenticity and natural flow throughout.")
        instructions.append("Ensure the blend feels cohesive, not frankensteined.")
        
        return " ".join(instructions)
    
    def _create_blend_summary(
        self,
        base_voice: Dict,
        influences: List[Tuple[Dict, float]]
    ) -> str:
        """Create a human-readable summary of the blend"""
        base_name = base_voice.get("metadata", {}).get("name", "Base")
        
        if not influences:
            return f"{base_name}'s voice (100%)"
        
        influence_strs = []
        for style_profile, weight in influences:
            name = style_profile.get("metadata", {}).get("name", "Unknown")
            percentage = int(weight * 100)
            influence_strs.append(f"{name} ({percentage}%)")
        
        return f"{base_name} + " + " + ".join(influence_strs)
    
    def create_generation_prompt(
        self,
        blended_style: Dict,
        content_brief: str,
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Create a complete prompt for AI content generation
        
        Args:
            blended_style: Output from blend_styles()
            content_brief: What to write about
            additional_instructions: Any extra requirements
            
        Returns:
            Complete prompt for AI
        """
        prompt_parts = [
            "# Content Generation Instructions\n",
            f"## Style Blend: {blended_style['blend_summary']}\n",
            f"\n{blended_style['composite_instructions']}\n",
            f"\n## Content Brief:\n{content_brief}\n"
        ]
        
        if additional_instructions:
            prompt_parts.append(f"\n## Additional Requirements:\n{additional_instructions}\n")
        
        # Add specific style elements
        prompt_parts.append("\n## Style Elements to Incorporate:\n")
        for influence in blended_style.get("influences", []):
            name = influence["name"]
            weight_pct = int(influence["weight"] * 100)
            prompt_parts.append(f"\n### From {name} ({weight_pct}%):\n")
            
            elements = influence["style_elements"]
            for category, items in elements.items():
                if items:
                    prompt_parts.append(f"- {category.replace('_', ' ').title()}: ")
                    prompt_parts.append(", ".join(str(k) for k, v in items.items() if v))
                    prompt_parts.append("\n")
        
        prompt_parts.append("\n## Output:\nGenerate the content following these style instructions.")
        
        return "".join(prompt_parts)
    
    def adjust_blend(
        self,
        current_blend: Dict,
        adjustments: Dict[str, float]
    ) -> Dict:
        """
        Adjust the weights of a blend
        
        Args:
            current_blend: Existing blend configuration
            adjustments: Dict of {influence_name: new_weight}
            
        Returns:
            Updated blend
        """
        # This would re-blend with adjusted weights
        # For now, just return instructions
        return {
            "message": "Blend adjustment not yet implemented",
            "current_blend": current_blend,
            "requested_adjustments": adjustments
        }


# Example usage
if __name__ == "__main__":
    # Mock style profiles for testing
    base_voice = {
        "metadata": {"name": "Louie Bernstein"},
        "style": {
            "sentence_structure": {"avg_sentence_length": 14, "fragment_ratio": 0.1},
            "vocabulary": {"reading_ease_score": 65},
            "rhetorical_devices": {"repetition_for_emphasis": 0.08},
            "emotional_tone": {"urgency_level": 0.008}
        }
    }
    
    hormozi_style = {
        "metadata": {"name": "Alex Hormozi"},
        "style": {
            "sentence_structure": {"avg_sentence_length": 10, "fragment_ratio": 0.25},
            "vocabulary": {"reading_ease_score": 75, "power_word_density": 0.02},
            "rhetorical_devices": {"contrast_usage": 0.35},
            "emotional_tone": {"urgency_level": 0.02, "confidence_level": 0.025}
        }
    }
    
    godin_style = {
        "metadata": {"name": "Seth Godin"},
        "style": {
            "sentence_structure": {"avg_sentence_length": 12, "fragment_ratio": 0.15},
            "vocabulary": {"reading_ease_score": 70},
            "rhetorical_devices": {"rule_of_threes": 0.08},
            "emotional_tone": {"sentiment_polarity": 0.4}
        }
    }
    
    blender = StyleBlender()
    
    # Create a blend
    blended = blender.blend_styles(
        base_voice=base_voice,
        influences=[
            (hormozi_style, 0.3),
            (godin_style, 0.2)
        ]
    )
    
    print("Blend Summary:", blended["blend_summary"])
    print("\nInstructions:")
    print(blended["composite_instructions"])
    
    # Generate a prompt
    prompt = blender.create_generation_prompt(
        blended_style=blended,
        content_brief="Write an article about sales team optimization",
        additional_instructions="Include 3 specific action items. Target length: 800 words."
    )
    
    print("\n" + "="*80)
    print("COMPLETE PROMPT:")
    print("="*80)
    print(prompt)

