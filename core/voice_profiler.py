"""
Voice Profiler - Create and manage individual voice profiles

This module handles:
- Creating voice profiles from content samples
- Saving/loading voice profiles
- Comparing voice similarity
- Voice consistency verification
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from .style_analyzer import StyleAnalyzer, StyleProfile


class VoiceProfiler:
    """Create and manage voice profiles"""
    
    def __init__(self, profiles_dir: str = "./data/voices"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.analyzer = StyleAnalyzer()
    
    def create_profile(
        self,
        name: str,
        content_samples: List[str],
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """
        Create a voice profile from content samples
        
        Args:
            name: Profile name (e.g., "Louie Bernstein")
            content_samples: List of text samples
            description: Optional description
            tags: Optional tags (e.g., ["sales", "consulting"])
            
        Returns:
            Complete voice profile dictionary
        """
        # Analyze the style
        style_profile = self.analyzer.analyze_samples(content_samples, name)
        
        # Create complete profile
        profile = {
            "metadata": {
                "name": name,
                "description": description or "",
                "tags": tags or [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "style": style_profile.to_dict(),
            "samples": {
                "count": len(content_samples),
                "total_words": style_profile.total_words,
                # Store first 500 chars of each sample for reference
                "excerpts": [sample[:500] for sample in content_samples[:3]]
            }
        }
        
        # Save profile
        self.save_profile(name, profile)
        
        return profile
    
    def load_profile(self, name: str) -> Optional[Dict]:
        """Load a voice profile by name"""
        profile_path = self._get_profile_path(name)
        
        if not profile_path.exists():
            return None
        
        with open(profile_path, 'r') as f:
            return json.load(f)
    
    def save_profile(self, name: str, profile: Dict):
        """Save a voice profile"""
        profile_path = self._get_profile_path(name)
        
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
    
    def list_profiles(self) -> List[Dict]:
        """List all available voice profiles"""
        profiles = []
        
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile = json.load(f)
                    
                    # Handle different profile formats
                    metadata = profile.get("metadata", {})
                    
                    # Get sample count from various possible locations
                    sample_count = 0
                    if "samples" in profile:
                        samples_info = profile["samples"]
                        if isinstance(samples_info, dict):
                            sample_count = samples_info.get("count", 0)
                    elif "llm_analysis" in profile:
                        # LLM-analyzed profile format
                        llm_analysis = profile.get("llm_analysis", {})
                        sample_count = llm_analysis.get("samples_analyzed", 0)
                    elif "style" in profile:
                        # Old format - check style profile
                        style = profile.get("style", {})
                        sample_count = style.get("sample_count", 0)
                    
                    profiles.append({
                        "name": metadata.get("name", profile_file.stem),
                        "description": metadata.get("description", ""),
                        "tags": metadata.get("tags", []),
                        "created_at": metadata.get("created_at", ""),
                        "sample_count": sample_count
                    })
            except Exception as e:
                # Skip corrupted profiles
                continue
        
        return profiles
    
    def update_profile(
        self,
        name: str,
        new_samples: List[str],
        append: bool = True
    ) -> Dict:
        """
        Update an existing voice profile with new samples
        
        Args:
            name: Profile name
            new_samples: New content samples
            append: If True, combine with existing; if False, replace
            
        Returns:
            Updated profile
        """
        existing_profile = self.load_profile(name)
        
        if not existing_profile:
            raise ValueError(f"Profile '{name}' not found")
        
        if append:
            # Would need to re-analyze with all samples combined
            # For now, just replace
            pass
        
        # Create new profile with new samples
        new_profile = self.create_profile(
            name=name,
            content_samples=new_samples,
            description=existing_profile["metadata"].get("description"),
            tags=existing_profile["metadata"].get("tags")
        )
        
        return new_profile
    
    def compare_voices(self, name1: str, name2: str) -> Dict[str, float]:
        """
        Compare similarity between two voice profiles
        
        Returns:
            Dictionary with similarity scores for different aspects
        """
        profile1 = self.load_profile(name1)
        profile2 = self.load_profile(name2)
        
        if not profile1 or not profile2:
            raise ValueError("One or both profiles not found")
        
        style1 = profile1["style"]
        style2 = profile2["style"]
        
        # Compare sentence structure
        sentence_sim = self._compare_dict_values(
            style1["sentence_structure"],
            style2["sentence_structure"]
        )
        
        # Compare vocabulary
        vocab_sim = self._compare_dict_values(
            style1["vocabulary"],
            style2["vocabulary"]
        )
        
        # Compare rhetorical devices
        rhetoric_sim = self._compare_dict_values(
            style1["rhetorical_devices"],
            style2["rhetorical_devices"]
        )
        
        # Compare emotional tone
        tone_sim = self._compare_dict_values(
            style1["emotional_tone"],
            style2["emotional_tone"]
        )
        
        # Overall similarity (average)
        overall = (sentence_sim + vocab_sim + rhetoric_sim + tone_sim) / 4
        
        return {
            "overall_similarity": round(overall, 3),
            "sentence_structure_similarity": round(sentence_sim, 3),
            "vocabulary_similarity": round(vocab_sim, 3),
            "rhetorical_similarity": round(rhetoric_sim, 3),
            "tone_similarity": round(tone_sim, 3)
        }
    
    def verify_content(self, name: str, content: str) -> Dict[str, Any]:
        """
        Verify if content matches a voice profile
        
        Args:
            name: Profile name
            content: Content to verify
            
        Returns:
            Verification results with match percentage and details
        """
        profile = self.load_profile(name)
        
        if not profile:
            raise ValueError(f"Profile '{name}' not found")
        
        # Analyze the new content
        new_analysis = self.analyzer.analyze_samples([content], "temp")
        
        # Compare with profile
        target_style = profile["style"]
        new_style = new_analysis.to_dict()
        
        # Calculate match scores
        sentence_match = self._compare_dict_values(
            target_style["sentence_structure"],
            new_style["sentence_structure"]
        )
        
        vocab_match = self._compare_dict_values(
            target_style["vocabulary"],
            new_style["vocabulary"]
        )
        
        rhetoric_match = self._compare_dict_values(
            target_style["rhetorical_devices"],
            new_style["rhetorical_devices"]
        )
        
        tone_match = self._compare_dict_values(
            target_style["emotional_tone"],
            new_style["emotional_tone"]
        )
        
        overall_match = (sentence_match + vocab_match + rhetoric_match + tone_match) / 4
        
        return {
            "matches_voice": overall_match >= 0.7,  # 70% threshold
            "match_score": round(overall_match * 100, 1),  # Convert to percentage
            "details": {
                "sentence_structure": round(sentence_match * 100, 1),
                "vocabulary": round(vocab_match * 100, 1),
                "rhetorical_devices": round(rhetoric_match * 100, 1),
                "emotional_tone": round(tone_match * 100, 1)
            },
            "recommendations": self._get_recommendations(overall_match, {
                "sentence": sentence_match,
                "vocab": vocab_match,
                "rhetoric": rhetoric_match,
                "tone": tone_match
            })
        }
    
    def _compare_dict_values(self, dict1: Dict, dict2: Dict) -> float:
        """
        Compare two dictionaries with numeric values
        Returns similarity score between 0 and 1
        """
        common_keys = set(dict1.keys()) & set(dict2.keys())
        
        if not common_keys:
            return 0.0
        
        differences = []
        for key in common_keys:
            val1 = dict1[key]
            val2 = dict2[key]
            
            # Skip non-numeric values
            if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)):
                continue
            
            # Normalize the difference
            if val1 == 0 and val2 == 0:
                diff = 0
            elif val1 == 0 or val2 == 0:
                diff = 1
            else:
                # Calculate relative difference
                diff = abs(val1 - val2) / max(abs(val1), abs(val2))
            
            differences.append(diff)
        
        if not differences:
            return 0.5  # No comparable values
        
        # Convert average difference to similarity score
        avg_diff = sum(differences) / len(differences)
        similarity = 1 - min(avg_diff, 1)
        
        return similarity
    
    def _get_recommendations(self, overall_match: float, details: Dict[str, float]) -> List[str]:
        """Generate recommendations for improving voice match"""
        recommendations = []
        
        if overall_match >= 0.9:
            recommendations.append("Excellent voice match!")
        elif overall_match >= 0.7:
            recommendations.append("Good voice match with minor differences")
        else:
            recommendations.append("Voice match could be improved")
        
        # Specific recommendations
        if details["sentence"] < 0.7:
            recommendations.append("Adjust sentence length and structure")
        
        if details["vocab"] < 0.7:
            recommendations.append("Use more characteristic vocabulary")
        
        if details["rhetoric"] < 0.7:
            recommendations.append("Incorporate more rhetorical devices")
        
        if details["tone"] < 0.7:
            recommendations.append("Adjust emotional tone and sentiment")
        
        return recommendations
    
    def _get_profile_path(self, name: str) -> Path:
        """Get file path for a profile"""
        # Sanitize name for filename
        safe_name = name.lower().replace(" ", "_").replace("/", "_")
        return self.profiles_dir / f"{safe_name}.json"


# Example usage
if __name__ == "__main__":
    profiler = VoiceProfiler()
    
    # Create a test profile
    samples = [
        """
        Here's the thing about sales that nobody tells you. You don't need more leads.
        You need a better process. Period.
        
        I've worked with over 100 companies. Same pattern every time.
        """,
        """
        Sales teams fail for three reasons: poor training, no accountability, and zero documentation.
        Fix those three things and you'll 10x your results. Guaranteed.
        """
    ]
    
    profile = profiler.create_profile(
        name="Test Author",
        content_samples=samples,
        description="Test sales consultant",
        tags=["sales", "consulting"]
    )
    
    print("Profile created:", profile["metadata"]["name"])
    print("\nAll profiles:")
    for p in profiler.list_profiles():
        print(f"  - {p['name']}: {p['sample_count']} samples")

