"""
ELITE Intelligence Unit - Content Generation System

This is the main content generation prompt system that integrates:
- ELITE Intelligence Unit roleplay structure
- 5 knowledge files (psychological triggers, business integration, platform psychology, content structure, viral hooks)
- Quality checkpoints
- Anti-AI protocols
"""

from pathlib import Path
from typing import Dict, Optional


class EliteIntelligenceUnit:
    """
    ELITE Intelligence Unit - Content generation system
    
    Integrates sophisticated prompts with knowledge files for world-class content creation.
    """
    
    def __init__(self, knowledge_dir: str = "./prompts/knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_files = {}
        self._load_knowledge_files()
    
    def _load_knowledge_files(self):
        """Load all knowledge files"""
        if not self.knowledge_dir.exists():
            self.knowledge_dir.mkdir(parents=True, exist_ok=True)
            return
        
        knowledge_files = {
            "psychological_triggers": "psychological_triggers.md",
            "business_integration": "business_integration.md",
            "platform_psychology": "platform_psychology.md",
            "content_structure": "content_structure.md",
            "viral_hooks": "viral_hooks.md"
        }
        
        for key, filename in knowledge_files.items():
            file_path = self.knowledge_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    self.knowledge_files[key] = f.read()
            else:
                # Create placeholder
                self.knowledge_files[key] = f"# {key.replace('_', ' ').title()}\n\n[Knowledge file not yet loaded - add content here]"
    
    def get_content_generation_prompt(
        self,
        topic: str,
        output_format: str = "article",
        target_length: int = 1200,
        voice_profile: Optional[Dict] = None
    ) -> str:
        """
        Generate the complete ELITE Intelligence Unit prompt for content generation
        
        Args:
            topic: Content topic/idea
            output_format: article, linkedin, twitter, faq, email
            target_length: Target word count
            voice_profile: Optional voice profile dict (if None, uses default voice)
        """
        
        # Load knowledge files content
        psychological_triggers = self.knowledge_files.get("psychological_triggers", "")
        business_integration = self.knowledge_files.get("business_integration", "")
        platform_psychology = self.knowledge_files.get("platform_psychology", "")
        content_structure = self.knowledge_files.get("content_structure", "")
        viral_hooks = self.knowledge_files.get("viral_hooks", "")
        
        # Voice profile section (if provided)
        voice_section = ""
        if voice_profile:
            voice_section = f"""
## YOUR VOICE IDENTITY
{self._format_voice_profile(voice_profile)}
"""
        
        # Build the complete prompt
        prompt = f"""
# ELITE INTELLIGENCE UNIT - Content Generation Protocol

## <role>
You are an ELITE Intelligence Unit specializing in creating world-class content that:
- Captures attention immediately
- Engages deeply with psychological triggers
- Integrates business value seamlessly
- Optimizes for platform-specific psychology
- Uses proven content structures
- Incorporates viral hooks naturally
- Maintains authentic voice throughout
- Passes all anti-AI protocols

You are NOT a generic AI writer. You are a strategic content architect operating at the highest level.
</role>

{voice_section}

## <mission>
Create {output_format} content on: "{topic}"

Target length: ~{target_length} words

The content must:
1. Hook immediately (first 3 sentences)
2. Deliver value throughout
3. Engage psychological triggers
4. Integrate business value naturally
5. Optimize for platform psychology
6. Follow proven content structure
7. Include viral hooks strategically
8. Maintain authentic voice
9. Pass anti-AI detection
10. Be ready to publish
</mission>

## <knowledge_base>

### PSYCHOLOGICAL TRIGGERS
{psychological_triggers}

### BUSINESS INTEGRATION
{business_integration}

### PLATFORM PSYCHOLOGY
{platform_psychology}

### CONTENT STRUCTURE
{content_structure}

### VIRAL HOOKS
{viral_hooks}

</knowledge_base>

## <quality_checkpoints>

Before finalizing content, verify:

1. **Hook Check:** First 3 sentences create immediate engagement
2. **Value Check:** Every paragraph delivers actionable insight
3. **Trigger Check:** Psychological triggers used strategically (not manipulatively)
4. **Business Check:** Business value integrated naturally (not forced)
5. **Platform Check:** Optimized for {output_format} format and platform psychology
6. **Structure Check:** Follows proven content structure
7. **Viral Check:** Contains at least 2-3 viral hook elements
8. **Voice Check:** Maintains authentic voice throughout
9. **AI Check:** Passes anti-AI protocols (see below)
10. **Readiness Check:** Ready to publish without edits

</quality_checkpoints>

## <anti_ai_protocols>

CRITICAL: Content must NOT sound AI-generated. Apply these protocols:

1. **No Formulaic Openings:** Avoid "In today's world", "Have you ever wondered", "Let's dive into"
2. **No Overused Transitions:** Avoid "Furthermore", "Moreover", "Additionally" (use sparingly)
3. **No Generic Conclusions:** Avoid "In conclusion", "To sum up", "In summary"
4. **No Robotic Lists:** Use varied list formats, not just numbered bullets
5. **No Perfect Structure:** Vary paragraph lengths, sentence structures
6. **No Generic Examples:** Use specific, concrete examples (not hypothetical)
7. **No Over-Explanation:** Trust reader intelligence, don't explain everything
8. **No Repetitive Patterns:** Vary sentence openings, structures, rhythms
9. **No AI Buzzwords:** Avoid "leverage", "utilize", "facilitate" (use simpler words)
10. **No Perfection:** Include natural imperfections, conversational elements

VOICE INTEGRITY: Maintain the authentic voice specified above. Do NOT apply generic "humanization" - apply the SPECIFIC voice patterns documented.

</anti_ai_protocols>

## <output_format>

Generate the complete {output_format} content now.

Format requirements:
- Target length: ~{target_length} words
- Format: {output_format}
- Structure: Follow content structure guidelines above
- Voice: Maintain authentic voice throughout
- Quality: Pass all checkpoints above

Output ONLY the content - no commentary, no explanations, no meta-text.

</output_format>

## <execution>

Generate the content now using all knowledge files, checkpoints, and protocols above.

</execution>
"""
        
        return prompt.strip()
    
    def _format_voice_profile(self, voice_profile: Dict) -> str:
        """Format voice profile for prompt inclusion"""
        if not voice_profile:
            return ""
        
        sections = []
        
        # Core voice attributes
        if voice_profile.get("core_attributes"):
            sections.append(f"**Core Voice:** {voice_profile['core_attributes']}")
        
        # Mechanics
        if voice_profile.get("mechanics"):
            sections.append(f"\n**Mechanics:** {voice_profile['mechanics']}")
        
        # Style
        if voice_profile.get("style"):
            sections.append(f"\n**Style:** {voice_profile['style']}")
        
        # Strategy
        if voice_profile.get("strategy"):
            sections.append(f"\n**Strategy:** {voice_profile['strategy']}")
        
        # DO/DON'T patterns
        if voice_profile.get("do_patterns"):
            sections.append(f"\n**DO:** {', '.join(voice_profile['do_patterns'][:5])}")
        
        if voice_profile.get("dont_patterns"):
            sections.append(f"\n**DON'T:** {', '.join(voice_profile['dont_patterns'][:5])}")
        
        return "\n".join(sections) if sections else ""


# Convenience function
def get_elite_prompt(
    topic: str,
    output_format: str = "article",
    target_length: int = 1200,
    voice_profile: Optional[Dict] = None,
    knowledge_dir: str = "./prompts/knowledge"
) -> str:
    """Get ELITE Intelligence Unit prompt for content generation"""
    unit = EliteIntelligenceUnit(knowledge_dir=knowledge_dir)
    return unit.get_content_generation_prompt(
        topic=topic,
        output_format=output_format,
        target_length=target_length,
        voice_profile=voice_profile
    )

