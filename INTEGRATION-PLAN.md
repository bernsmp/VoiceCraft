# VoiceCraft Integration Plan: Your Prompts + Code Structure

## 🎯 The Vision

**Hybrid System:** Combine your sophisticated prompts (LLM-powered analysis) with the code structure (automation, CLI, storage) for the best of both worlds.

---

## ✅ What We're Keeping

### Code Structure (Automation Layer)
- ✅ CLI tool for easy usage
- ✅ Profile storage/management
- ✅ Style blending logic
- ✅ Content generation pipeline
- ✅ Multi-format output
- ✅ Auto-publishing integrations

### Your Prompts (Analysis Layer)
- ✅ Personal & Brand Voice Guide (3-level analysis)
- ✅ Voice Connoisseur (discover through heroes)
- ✅ AI Text Humanizer (personalized)
- ✅ Voice-Avatar Alignment Optimizer
- ✅ Speaker Detection & Voice Pack
- ✅ Master AI-ism List

---

## 🔄 How They Work Together

### Architecture

```
┌─────────────────────────────────────────┐
│         CLI / API Interface              │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌─────────▼──────────┐
│ Rule-Based     │    │ LLM-Based          │
│ Analyzer       │    │ Analyzer           │
│                │    │                    │
│ - Fast         │    │ - Deep             │
│ - Consistent   │    │ - Nuanced          │
│ - Quantifiable │    │ - Human-like       │
└───────┬────────┘    └─────────┬──────────┘
        │                       │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   Unified Profile     │
        │   Storage System      │
        └───────────────────────┘
```

### Workflow Options

**Option 1: Quick Analysis (Rule-Based)**
```bash
# Fast, consistent, good for initial profiling
voicecraft profile create --name "Author" --samples "./*.md"
```

**Option 2: Deep Analysis (LLM-Powered)**
```bash
# Uses your sophisticated prompts for nuanced analysis
voicecraft profile create-deep --name "Author" \
  --samples "./*.md" \
  --avatar "./avatar.json" \
  --use-llm-analysis
```

**Option 3: Hybrid (Best of Both)**
```bash
# Rule-based for structure, LLM for depth
voicecraft profile create-hybrid --name "Author" \
  --samples "./*.md" \
  --avatar "./avatar.json"
```

---

## 📋 Integration Steps

### Phase 1: Add LLM Analyzer Module ✅
- [x] Created `core/llm_voice_analyzer.py`
- [x] Created `prompts/voice_analysis_prompts.py`
- [x] Integrated all your prompts

### Phase 2: Update CLI Commands
- [ ] Add `--use-llm` flag to profile creation
- [ ] Add `voice-connoisseur` command
- [ ] Add `humanizer-generate` command
- [ ] Add `friction-finder` command
- [ ] Add `speaker-detect` command

### Phase 3: Unified Profile Format
- [ ] Extend profile schema to include LLM analysis
- [ ] Merge rule-based + LLM results
- [ ] Store both analysis types

### Phase 4: Enhanced Content Generation
- [ ] Use LLM profiles for better style blending
- [ ] Integrate AI humanizer into generation pipeline
- [ ] Apply avatar alignment automatically

---

## 🎨 New CLI Commands (Planned)

### Voice Connoisseur
```bash
# Discover voice through admired writers
voicecraft voice-connoisseur \
  --transcript "./my-heroes-transcript.txt" \
  --output "./voice-discovery.json"
```

### Deep Profile Creation
```bash
# Full 3-level analysis with avatar alignment
voicecraft profile create-deep \
  --name "Author" \
  --samples "./samples/*.md" \
  --avatar "./avatar-blueprint.json" \
  --voice-connoisseur "./heroes-analysis.json" \
  --brand-context "./website-content.md"
```

### AI Humanizer Generator
```bash
# Generate personalized humanizer prompt
voicecraft humanizer-generate \
  --profile "Author" \
  --avatar "./avatar.json" \
  --output "./my-humanizer-prompt.md"
```

### Friction Finder
```bash
# Find voice-avatar misalignments
voicecraft friction-finder \
  --profile "Author" \
  --avatar "./avatar.json" \
  --output "./adjustment-rules.md"
```

### Speaker Detection
```bash
# Analyze transcripts for voice extraction
voicecraft speaker-detect \
  --transcripts "./interviews/*.txt" \
  --speaker "John Doe" \
  --output "./voice-pack.json"
```

---

## 💡 Usage Examples

### Complete Workflow

**Step 1: Discover Your Voice (Voice Connoisseur)**
```bash
# User writes transcript about admired writers
voicecraft voice-connoisseur --transcript "./my-heroes.txt"
# Output: voice-discovery.json
```

**Step 2: Create Deep Profile**
```bash
voicecraft profile create-deep \
  --name "Max" \
  --samples "./my-content/*.md" \
  --avatar "./my-avatar.json" \
  --voice-connoisseur "./voice-discovery.json" \
  --use-llm-analysis
# Output: Complete Personal & Brand Voice Guide
```

**Step 3: Find Friction Points**
```bash
voicecraft friction-finder \
  --profile "Max" \
  --avatar "./my-avatar.json"
# Output: 5 adjustment rules
```

**Step 4: Generate Humanizer**
```bash
voicecraft humanizer-generate \
  --profile "Max" \
  --avatar "./my-avatar.json"
# Output: Personalized AI Text Humanizer prompt
```

**Step 5: Generate Content**
```bash
voicecraft generate article \
  --profile "Max" \
  --topic "Sales optimization" \
  --influences "Hormozi:0.3" \
  --humanize  # Auto-applies humanizer
```

---

## 🔧 Technical Implementation

### Profile Schema Extension

```json
{
  "metadata": {
    "name": "Author",
    "created_at": "2025-11-24",
    "analysis_type": "hybrid"  // "rule-based" | "llm" | "hybrid"
  },
  "rule_based_analysis": {
    // Existing StyleProfile data
  },
  "llm_analysis": {
    "personal_voice_guide": {},
    "brand_voice_guide": {},
    "mechanics": {},
    "style": {},
    "strategy": {}
  },
  "voice_connoisseur": {
    "admired_writers": [],
    "shared_patterns": {},
    "hidden_insights": {}
  },
  "avatar_alignment": {
    "friction_points": [],
    "adjustment_rules": []
  }
}
```

### Cost Considerations

**Rule-Based:** Free, instant, consistent  
**LLM-Based:** ~$0.10-0.50 per analysis, 30-60 seconds, nuanced

**Recommendation:** Use rule-based for quick checks, LLM for final profiles.

---

## 🚀 Next Steps

### Immediate (This Week)
1. ✅ Created LLM analyzer module
2. ✅ Integrated all prompts
3. [ ] Test LLM analyzer with real content
4. [ ] Update CLI to use LLM analyzer
5. [ ] Create unified profile format

### Short Term (Next 2 Weeks)
1. [ ] Add all new CLI commands
2. [ ] Build hybrid analysis workflow
3. [ ] Integrate humanizer into generation
4. [ ] Test with Louie's content
5. [ ] Test with Jay's content

### Medium Term (Next Month)
1. [ ] Web dashboard with LLM analysis
2. [ ] Batch processing for multiple profiles
3. [ ] Voice evolution tracking
4. [ ] Performance optimization

---

## 💎 The Value Proposition

### Before (Rule-Based Only)
- Fast, consistent analysis
- Good for initial profiling
- Limited nuance

### After (Hybrid System)
- ✅ Fast initial analysis (rule-based)
- ✅ Deep, nuanced analysis (LLM)
- ✅ Voice discovery through heroes
- ✅ Avatar alignment optimization
- ✅ Personalized AI humanization
- ✅ Complete workflow automation

---

## 🎯 Decision: Use Your Prompts

**YES - These are superior!**

Your prompts provide:
- ✅ Deeper analysis (3-level: Mechanics → Style → Strategy)
- ✅ Avatar alignment (critical for client work)
- ✅ Voice Connoisseur (unique differentiator)
- ✅ AI-ism detection (practical value)
- ✅ More nuanced understanding

**Integration Strategy:**
- Use your prompts for **deep analysis** (final profiles)
- Keep rule-based for **quick checks** (initial profiling)
- Combine both in **hybrid mode** (best of both worlds)

---

## 📝 Implementation Status

- [x] Created LLM analyzer module
- [x] Integrated all prompts
- [x] Created integration plan
- [ ] Update CLI commands
- [ ] Test with real content
- [ ] Deploy hybrid system

**Ready to integrate!** 🚀

