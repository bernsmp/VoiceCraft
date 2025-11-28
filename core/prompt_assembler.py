"""
Prompt Assembler - Loads and assembles modular prompt files

This module loads the modular prompt structure and assembles complete prompts
for content generation based on input type and requirements.
"""

from pathlib import Path
from typing import Dict, List, Optional
import os


class PromptAssembler:
    """Assemble prompts from modular files"""
    
    def __init__(self, prompts_dir: str = "./prompts"):
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}
    
    def load_file(self, relative_path: str) -> str:
        """Load a prompt file, with caching"""
        if relative_path in self._cache:
            return self._cache[relative_path]
        
        file_path = self.prompts_dir / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._cache[relative_path] = content
        return content
    
    def build_prompt(
        self,
        user_input: str,
        input_type: str = "topic",
        platforms: Optional[List[str]] = None,
        include_viral: bool = True,
        include_platforms: bool = True,
        include_multiplication: bool = False
    ) -> str:
        """
        Assemble complete prompt from modular components
        
        Args:
            user_input: The input content/topic/idea
            input_type: Type of input (voice_note, transcript, idea, existing, analytics, comments, topic)
            platforms: List of platforms to optimize for
            include_viral: Include viral psychology framework
            include_platforms: Include platform optimization
            include_multiplication: Include content multiplication framework
        """
        
        # Always load core files
        prompt_parts = []
        
        # Load voice profile
        try:
            voice_profile = self.load_file("core/voice_profile_max.md")
            prompt_parts.append(f"<voice_profile>\n{voice_profile}\n</voice_profile>")
        except FileNotFoundError:
            pass  # Skip if not available
        
        # Load anti-AI patterns
        try:
            anti_ai = self.load_file("core/anti_ai_patterns.md")
            prompt_parts.append(f"<anti_ai_enforcement>\n{anti_ai}\n</anti_ai_enforcement>")
        except FileNotFoundError:
            pass
        
        # Load input-specific processing
        if input_type in ['voice_note', 'transcript', 'idea', 'existing', 'analytics', 'comments']:
            try:
                input_processing = self.load_file("frameworks/input_processing.md")
                prompt_parts.append(f"<input_processing>\n{input_processing}\n</input_processing>")
            except FileNotFoundError:
                pass
        
        # Always load hook engineering
        try:
            hook_engineering = self.load_file("frameworks/hook_engineering.md")
            prompt_parts.append(f"<hook_engineering>\n{hook_engineering}\n</hook_engineering>")
        except FileNotFoundError:
            pass
        
        # Always load content structure
        try:
            content_structure = self.load_file("frameworks/content_structure.md")
            prompt_parts.append(f"<content_structure>\n{content_structure}\n</content_structure>")
        except FileNotFoundError:
            pass
        
        # Load viral psychology if requested
        if include_viral:
            try:
                viral_psychology = self.load_file("frameworks/viral_psychology.md")
                prompt_parts.append(f"<viral_psychology>\n{viral_psychology}\n</viral_psychology>")
            except FileNotFoundError:
                pass
        
        # Load platform optimization if multiple platforms or requested
        if include_platforms and (platforms and len(platforms) > 1):
            try:
                platform_optimization = self.load_file("frameworks/platform_optimization.md")
                prompt_parts.append(f"<platform_optimization>\n{platform_optimization}\n</platform_optimization>")
            except FileNotFoundError:
                pass
        
        # Load content multiplication if requested
        if include_multiplication:
            try:
                content_multiplication = self.load_file("frameworks/content_multiplication.md")
                prompt_parts.append(f"<content_multiplication>\n{content_multiplication}\n</content_multiplication>")
            except FileNotFoundError:
                pass
        
        # Load output schema
        try:
            output_schema = self.load_file("core/output_schema.md")
            prompt_parts.append(f"<output_format>\n{output_schema}\n</output_format>")
        except FileNotFoundError:
            pass
        
        # Build the complete prompt
        prompt = f"""<role>
You are generating content as Max Bernstein. You write for sophisticated builders and experts who want mechanisms, not motivation. Your voice is confident, specific, and story-driven.
</role>

{chr(10).join(prompt_parts)}

<input_content>
{user_input}
</input_content>

<task>
Transform the input into viral content following Max's voice and structure patterns.

1. Analyze the input for energy, key phrases, and story seeds
2. Identify 3-5 viral moments with psychological triggers
3. Generate primary hook using status threat + paradox formula
4. Build full content following the winning structure
5. Create platform variations (if platforms specified)
6. Score quality and flag any violations
</task>

<verification_checkpoint>
Before outputting, verify:

□ Hook grabs in first 3 words (no warm-up)?
□ Zero banned AI patterns present?
□ Matches voice calibration examples?
□ Specific numbers included (not vague claims)?
□ Story-first structure (concrete → abstract → concrete)?
□ List density meets target (8-18 for long-form)?
□ Paragraph average under 10 words?

If ANY check fails, revise before outputting.
</verification_checkpoint>
"""
        
        return prompt.strip()
    
    def build_from_template(self, user_input: str) -> str:
        """Build prompt using the assembly template"""
        try:
            template = self.load_file("assembly/content_generator_prompt.md")
            
            # Replace placeholders
            prompt = template
            
            # Replace INSERT placeholders
            replacements = {
                "{{INSERT: core/voice_profile_max.md}}": self.load_file("core/voice_profile_max.md"),
                "{{INSERT: core/anti_ai_patterns.md}}": self.load_file("core/anti_ai_patterns.md"),
                "{{INSERT: frameworks/hook_engineering.md}}": self.load_file("frameworks/hook_engineering.md"),
                "{{INSERT: frameworks/content_structure.md}}": self.load_file("frameworks/content_structure.md"),
                "{{INSERT: core/output_schema.md}}": self.load_file("core/output_schema.md"),
                "{{USER_INPUT_HERE}}": user_input
            }
            
            for placeholder, content in replacements.items():
                prompt = prompt.replace(placeholder, content)
            
            return prompt
            
        except FileNotFoundError as e:
            # Fallback to build_prompt method
            return self.build_prompt(user_input)


# Convenience function
def build_content_prompt(
    user_input: str,
    input_type: str = "topic",
    platforms: Optional[List[str]] = None,
    prompts_dir: str = "./prompts"
) -> str:
    """Build content generation prompt from modular files"""
    assembler = PromptAssembler(prompts_dir=prompts_dir)
    return assembler.build_prompt(
        user_input=user_input,
        input_type=input_type,
        platforms=platforms or [],
        include_viral=True,
        include_platforms=bool(platforms),
        include_multiplication=bool(platforms and len(platforms) > 1)
    )

