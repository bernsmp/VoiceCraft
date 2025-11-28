"""
Prompt Library - Pre-built writer prompts for Style Fusion

These are sophisticated prompts for different writing styles that can be
used as influences in style fusion.
"""

from pathlib import Path
from typing import Dict, Optional


class PromptLibrary:
    """Manage library of writer prompts for style fusion"""
    
    def __init__(self, prompts_dir: str = "./writing prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
        """Load all prompts from the writing prompts directory"""
        if not self.prompts_dir.exists():
            return
        
        for prompt_file in self.prompts_dir.glob("*.md"):
            writer_name = prompt_file.stem.replace("_", " ").title()
            
            with open(prompt_file, 'r') as f:
                content = f.read()
            
            self.prompts[writer_name] = {
                "name": writer_name,
                "prompt": content,
                "file": str(prompt_file),
                "type": self._detect_prompt_type(content)
            }
    
    def _detect_prompt_type(self, content: str) -> str:
        """Detect what type of prompt this is"""
        content_lower = content.lower()
        
        if "narrative hook" in content_lower or "gladwell" in content_lower:
            return "narrative_hook"
        elif "actionable framework" in content_lower or "clear" in content_lower:
            return "actionable_framework"
        elif "contrarian" in content_lower or "graham" in content_lower:
            return "contrarian_essay"
        elif "timeless principle" in content_lower or "housel" in content_lower:
            return "timeless_principle"
        elif "explainer" in content_lower or "urban" in content_lower:
            return "explainer"
        else:
            return "general"
    
    def get_prompt(self, writer_name: str) -> Optional[Dict]:
        """Get prompt for a specific writer"""
        # Try exact match
        if writer_name in self.prompts:
            return self.prompts[writer_name]
        
        # Try case-insensitive match
        for name, prompt_data in self.prompts.items():
            if name.lower() == writer_name.lower():
                return prompt_data
        
        # Try partial match
        for name, prompt_data in self.prompts.items():
            if writer_name.lower() in name.lower() or name.lower() in writer_name.lower():
                return prompt_data
        
        return None
    
    def list_writers(self) -> list:
        """List all available writers"""
        return list(self.prompts.keys())
    
    def get_prompt_text(self, writer_name: str) -> Optional[str]:
        """Get just the prompt text"""
        prompt_data = self.get_prompt(writer_name)
        return prompt_data["prompt"] if prompt_data else None


# Global instance
_prompt_library = None

def get_prompt_library() -> PromptLibrary:
    """Get or create global prompt library instance"""
    global _prompt_library
    if _prompt_library is None:
        _prompt_library = PromptLibrary()
    return _prompt_library

