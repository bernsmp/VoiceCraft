"""
Style Analyzer - Extract writing patterns from content samples

This module analyzes text to extract:
- Sentence structure patterns
- Vocabulary preferences
- Rhetorical devices
- Emotional tone
- Content flow patterns
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import json

try:
    import spacy
    import textstat
    from textblob import TextBlob
except ImportError:
    print("Warning: Some NLP libraries not installed. Install with: pip install spacy textstat textblob")


@dataclass
class StyleProfile:
    """Complete style profile of a writer"""
    name: str
    sentence_structure: Dict[str, float]
    vocabulary: Dict[str, Any]
    rhetorical_devices: Dict[str, float]
    emotional_tone: Dict[str, float]
    content_flow: Dict[str, Any]
    sample_count: int
    total_words: int
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StyleProfile':
        return cls(**data)


class StyleAnalyzer:
    """Analyze writing style from content samples"""
    
    def __init__(self):
        # Try to load spaCy model, but don't fail if not available
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not loaded. Some features will be limited.")
            self.nlp = None
    
    def analyze_samples(self, samples: List[str], author_name: str = "Unknown") -> StyleProfile:
        """
        Analyze multiple content samples to create a style profile
        
        Args:
            samples: List of text samples (articles, posts, etc.)
            author_name: Name of the author
            
        Returns:
            StyleProfile object with extracted patterns
        """
        # Combine all samples for analysis
        combined_text = "\n\n".join(samples)
        
        return StyleProfile(
            name=author_name,
            sentence_structure=self._analyze_sentence_structure(samples),
            vocabulary=self._analyze_vocabulary(combined_text),
            rhetorical_devices=self._analyze_rhetorical_devices(samples),
            emotional_tone=self._analyze_emotional_tone(combined_text),
            content_flow=self._analyze_content_flow(samples),
            sample_count=len(samples),
            total_words=len(combined_text.split())
        )
    
    def _analyze_sentence_structure(self, samples: List[str]) -> Dict[str, float]:
        """Analyze sentence structure patterns"""
        all_sentences = []
        for sample in samples:
            # Split into sentences (simple approach)
            sentences = re.split(r'[.!?]+', sample)
            sentences = [s.strip() for s in sentences if s.strip()]
            all_sentences.extend(sentences)
        
        if not all_sentences:
            return {}
        
        # Calculate metrics
        sentence_lengths = [len(s.split()) for s in all_sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        
        # Count fragments (sentences < 5 words)
        fragments = sum(1 for length in sentence_lengths if length < 5)
        fragment_ratio = fragments / len(all_sentences)
        
        # Count questions
        questions = sum(1 for s in all_sentences if '?' in s)
        question_frequency = questions / len(all_sentences)
        
        # Count exclamations
        exclamations = sum(1 for s in all_sentences if '!' in s)
        exclamation_frequency = exclamations / len(all_sentences)
        
        return {
            "avg_sentence_length": round(avg_length, 2),
            "fragment_ratio": round(fragment_ratio, 3),
            "question_frequency": round(question_frequency, 3),
            "exclamation_frequency": round(exclamation_frequency, 3),
            "sentence_count": len(all_sentences),
            "length_variance": round(self._calculate_variance(sentence_lengths), 2)
        }
    
    def _analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """Analyze vocabulary patterns"""
        words = text.lower().split()
        
        # Reading level
        try:
            reading_ease = textstat.flesch_reading_ease(text)
            grade_level = textstat.flesch_kincaid_grade(text)
        except:
            reading_ease = 0
            grade_level = 0
        
        # Word length
        word_lengths = [len(w.strip('.,!?;:')) for w in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
        
        # Common power words
        power_words = [
            'guaranteed', 'proven', 'results', 'immediately', 'literally',
            'obviously', 'actually', 'specifically', 'exactly', 'ultimately'
        ]
        power_word_count = sum(1 for word in words if word.strip('.,!?;:') in power_words)
        power_word_density = power_word_count / len(words) if words else 0
        
        return {
            "avg_word_length": round(avg_word_length, 2),
            "reading_ease_score": round(reading_ease, 2),
            "grade_level": round(grade_level, 2),
            "total_words": len(words),
            "unique_words": len(set(words)),
            "lexical_diversity": round(len(set(words)) / len(words), 3) if words else 0,
            "power_word_density": round(power_word_density, 4)
        }
    
    def _analyze_rhetorical_devices(self, samples: List[str]) -> Dict[str, float]:
        """Analyze use of rhetorical devices"""
        combined = " ".join(samples)
        sentences = re.split(r'[.!?]+', combined)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Repetition patterns (simple approach)
        words = combined.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 5:  # Only count substantial words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repeated_words = sum(1 for count in word_freq.values() if count > 3)
        repetition_score = repeated_words / len(word_freq) if word_freq else 0
        
        # Contrast patterns ("not X, Y" or "X but Y")
        contrast_patterns = [
            r'\bnot\b.*\bbut\b',
            r'\binstead\b',
            r'\bhowever\b',
            r'\byet\b'
        ]
        contrast_count = sum(len(re.findall(pattern, combined.lower())) for pattern in contrast_patterns)
        contrast_usage = contrast_count / len(sentences) if sentences else 0
        
        # Rule of threes (lists of three items)
        three_pattern = r'\b\w+\s*,\s*\w+\s*,\s*(and|or)\s+\w+\b'
        rule_of_three_count = len(re.findall(three_pattern, combined))
        rule_of_three_frequency = rule_of_three_count / len(sentences) if sentences else 0
        
        return {
            "repetition_for_emphasis": round(repetition_score, 3),
            "contrast_usage": round(contrast_usage, 3),
            "rule_of_threes": round(rule_of_three_frequency, 3)
        }
    
    def _analyze_emotional_tone(self, text: str) -> Dict[str, float]:
        """Analyze emotional tone and sentiment"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
        except:
            polarity = 0
            subjectivity = 0.5
        
        # Urgency indicators
        urgency_words = ['now', 'immediately', 'today', 'urgent', 'quick', 'fast', 'hurry']
        words = text.lower().split()
        urgency_count = sum(1 for word in words if word.strip('.,!?;:') in urgency_words)
        urgency_score = urgency_count / len(words) if words else 0
        
        # Confidence indicators
        confidence_words = ['will', 'must', 'guaranteed', 'proven', 'certain', 'definitely']
        confidence_count = sum(1 for word in words if word.strip('.,!?;:') in confidence_words)
        confidence_score = confidence_count / len(words) if words else 0
        
        return {
            "sentiment_polarity": round(polarity, 3),  # -1 (negative) to 1 (positive)
            "subjectivity": round(subjectivity, 3),  # 0 (objective) to 1 (subjective)
            "urgency_level": round(urgency_score, 4),
            "confidence_level": round(confidence_score, 4)
        }
    
    def _analyze_content_flow(self, samples: List[str]) -> Dict[str, Any]:
        """Analyze content structure and flow"""
        # Analyze opening patterns
        openings = [sample[:200] for sample in samples if len(sample) > 200]
        
        hook_types = {
            "question": 0,
            "statistic": 0,
            "bold_claim": 0,
            "story": 0
        }
        
        for opening in openings:
            if '?' in opening[:100]:
                hook_types["question"] += 1
            if re.search(r'\d+%|\$\d+|[0-9]{2,}', opening[:100]):
                hook_types["statistic"] += 1
            if any(word in opening.lower()[:100] for word in ['never', 'always', 'everyone', 'nobody']):
                hook_types["bold_claim"] += 1
            if any(word in opening.lower()[:100] for word in ['when i', 'story', 'once', 'remember']):
                hook_types["story"] += 1
        
        # Normalize
        total = len(openings) if openings else 1
        hook_distribution = {k: round(v/total, 3) for k, v in hook_types.items()}
        
        # Average paragraph length (rough estimate based on double newlines)
        avg_para_length = []
        for sample in samples:
            paragraphs = sample.split('\n\n')
            para_lengths = [len(p.split()) for p in paragraphs if p.strip()]
            if para_lengths:
                avg_para_length.append(sum(para_lengths) / len(para_lengths))
        
        return {
            "hook_distribution": hook_distribution,
            "avg_paragraph_length": round(sum(avg_para_length) / len(avg_para_length), 2) if avg_para_length else 0
        }
    
    def _calculate_variance(self, numbers: List[float]) -> float:
        """Calculate variance of a list of numbers"""
        if not numbers:
            return 0
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        return variance


# Example usage
if __name__ == "__main__":
    # Test with sample text
    samples = [
        """
        Here's the thing about sales that nobody tells you. You don't need more leads.
        You need a better process. Period.
        
        I've worked with over 100 companies. Same pattern every time. They think it's a pipeline problem.
        It's not. It's a process problem.
        
        Want proof? Let me show you exactly what I mean.
        """,
        """
        Sales teams fail for three reasons: poor training, no accountability, and zero documentation.
        Fix those three things and you'll 10x your results. Guaranteed.
        
        The best part? It's not complicated. You just need someone who's done it before.
        That's where I come in.
        """
    ]
    
    analyzer = StyleAnalyzer()
    profile = analyzer.analyze_samples(samples, "Test Author")
    
    print("Style Profile:")
    print(profile.to_json())

