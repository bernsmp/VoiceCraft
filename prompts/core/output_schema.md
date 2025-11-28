## REQUIRED OUTPUT STRUCTURE

All content generation must return this JSON structure:

```json
{
  "voice_analysis": {
    "detected_energy": "string (excited/frustrated/curious/determined/reflective)",
    "key_phrases": ["array of powerful phrases from input worth preserving"],
    "story_seeds": ["potential narrative anchors detected"]
  },
  
  "viral_moments": [
    {
      "moment": "the specific insight/story/revelation",
      "why_viral": "psychological trigger it activates",
      "hook_angle": "how to open with this"
    }
  ],
  
  "primary_content": {
    "hook": {
      "text": "Under 15 words, first-second impact",
      "type": "discovery|transformation|problem-solution|urgency|authority|curiosity|relatable",
      "status_threat": "what reader is losing/missing (not gaining)"
    },
    "structure": [
      {
        "section": "hook",
        "content": "...",
        "word_count": 0,
        "lists_included": 0
      },
      {
        "section": "story_anchor",
        "content": "...",
        "word_count": 0,
        "lists_included": 0
      },
      {
        "section": "principle_extraction",
        "content": "...",
        "word_count": 0,
        "lists_included": 0
      },
      {
        "section": "application",
        "content": "...",
        "word_count": 0,
        "lists_included": 0
      },
      {
        "section": "mechanism",
        "content": "...",
        "word_count": 0,
        "lists_included": 0
      }
    ],
    "total_lists": "integer (target: 8-18 for long-form)",
    "avg_paragraph_words": "float (target: 6-10)"
  },
  
  "variations": [
    {
      "platform": "tiktok|instagram|youtube|linkedin",
      "adjusted_hook": "platform-optimized version",
      "structure_notes": "what changes for this platform",
      "timing": "content duration/length"
    }
  ],
  
  "quality_scores": {
    "voice_match": "integer 0-100",
    "hook_strength": "integer 0-100",
    "list_density": "integer 0-100",
    "specificity": "integer 0-100",
    "ai_pattern_check": "pass|fail",
    "banned_patterns_found": ["array of any violations detected"]
  }
}
```

---

## QUALITY THRESHOLDS

| Metric | Minimum | Target |
|--------|---------|--------|
| voice_match | 75 | 90+ |
| hook_strength | 70 | 85+ |
| list_density | 60 | 80+ |
| specificity | 75 | 90+ |
| ai_pattern_check | pass | pass |

If any score falls below minimum, flag for revision before output.

