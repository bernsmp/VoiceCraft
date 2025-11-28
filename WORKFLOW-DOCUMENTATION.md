# VoiceCraft Complete Workflow Documentation

## 🎯 How Everything Works Together

This document shows the complete flow from input to published content, including how all the systems integrate.

---

## 📊 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
│  Voice Notes | Topics | Transcripts | Ideas | Comments          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW AUTOMATION                          │
│  • Auto-detect input type                                       │
│  • Auto-detect output format                                    │
│  • Process input (clean, extract, structure)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CONTENT GENERATOR                             │
│  • Load voice profile (Max Bernstein)                          │
│  • Assemble modular prompts                                    │
│  • Generate content with AI                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MODULAR PROMPT SYSTEM                          │
│  • Voice Profile (Max's patterns)                               │
│  • Hook Engineering (status threat formulas)                    │
│  • Content Structure (8-section winning format)                │
│  • Anti-AI Patterns (banned phrases removed)                    │
│  • Viral Psychology (7 sharing drivers)                         │
│  • Platform Optimization (if specified)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI GENERATION                              │
│  • Claude/GPT generates content                                 │
│  • Follows all prompt guidelines                                │
│  • Returns structured output                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HUMANIZER                                  │
│  • Removes AI-isms                                              │
│  • Maintains voice integrity                                    │
│  • Applies Max's specific patterns                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PUBLISHING                                 │
│  • GitHub (auto-commit)                                         │
│  • WordPress (auto-publish)                                    │
│  • File (save locally)                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Step-by-Step Workflow

### Step 1: Input Detection

**What happens:**
```python
workflow = ContentWorkflow("Max Bernstein")
result = workflow.process_input("Your voice note or topic here")
```

**Auto-detection logic:**
- **Voice Note:** Detects speech patterns, filler words, conversational flow
- **WhatsApp:** Detects timestamps, chat format
- **Bullet Points:** Detects list markers (-, *, •, 1., 2.)
- **Topic:** Default for everything else

**Output Format Detection:**
- **LinkedIn:** Short inputs (<30 words), mentions "linkedin"
- **Twitter:** Mentions "twitter", "tweet", "thread"
- **FAQ:** Mentions "faq", "question", "q&a"
- **Email:** Mentions "email", "newsletter"
- **Article:** Default for longer inputs (50+ words)

---

### Step 2: Input Processing

**Voice Note Processing:**
```python
# Removes filler words
# Preserves energy and exact phrases
# Extracts story seeds and quotable moments
```

**Bullet Points Processing:**
```python
# Converts to narrative brief
# Removes bullet markers
# Structures as content brief
```

**WhatsApp Processing:**
```python
# Removes metadata (timestamps, names)
# Extracts conversation content
# Structures as narrative
```

---

### Step 3: Prompt Assembly

**What happens:**
```python
# ContentGenerator calls PromptAssembler
assembler = PromptAssembler()

# Loads modular files:
# 1. core/voice_profile_max.md
# 2. core/anti_ai_patterns.md
# 3. frameworks/hook_engineering.md
# 4. frameworks/content_structure.md
# 5. frameworks/viral_psychology.md
# 6. frameworks/platform_optimization.md (if platforms specified)
# 7. frameworks/input_processing.md (based on input_type)
# 8. core/output_schema.md

prompt = assembler.build_prompt(
    user_input=content_brief,
    input_type="voice_note",
    platforms=["linkedin"]
)
```

**Prompt Structure:**
```
<role>
You are generating content as Max Bernstein...
</role>

<voice_profile>
[Your exact voice patterns - Scene Drop, Triple Beat, etc.]
</voice_profile>

<anti_ai_enforcement>
[Banned patterns with replacements]
</anti_ai_enforcement>

<hook_engineering>
[Status threat hierarchy, hook formulas]
</hook_engineering>

<content_structure>
[8-section winning structure, metrics]
</content_structure>

<viral_psychology>
[7 core sharing drivers]
</viral_psychology>

<input_content>
[Your actual input]
</input_content>

<task>
[Step-by-step generation instructions]
</task>

<verification_checkpoint>
[Quality checks before output]
</verification_checkpoint>
```

---

### Step 4: Content Generation

**What happens:**
```python
# ContentGenerator sends prompt to Claude/GPT
# AI generates content following all guidelines
# Returns structured output
```

**Generation Process:**
1. Analyzes input for energy, key phrases, story seeds
2. Identifies 3-5 viral moments with psychological triggers
3. Generates hook using status threat + paradox formula
4. Builds content following 8-section structure
5. Creates platform variations (if platforms specified)
6. Scores quality and flags violations

**Quality Checks:**
- Hook grabs in first 3 words? ✓
- Zero banned AI patterns? ✓
- Matches voice calibration? ✓
- Specific numbers included? ✓
- Story-first structure? ✓
- List density 8-18? ✓
- Paragraph average <10 words? ✓

---

### Step 5: Humanization

**What happens:**
```python
humanizer = Humanizer(profile_name="Max Bernstein")
humanized = humanizer.humanize(
    text=generated_content,
    show_analysis=False
)
```

**Humanization Process:**
1. Scans for AI-isms (banned patterns)
2. Removes generic phrases
3. Applies Max's specific voice patterns
4. Maintains voice integrity
5. Returns humanized content

---

### Step 6: Publishing (Optional)

**GitHub Publishing:**
```python
publish_config = {
    "destination": "github",
    "repo": "username/repo",
    "file_path": "content/articles/my-article.md"
}
```

**WordPress Publishing:**
```python
publish_config = {
    "destination": "wordpress",
    "site_url": "yoursite.com",
    "app_password": "xxxx xxxx xxxx xxxx",
    "status": "draft"
}
```

---

## 🎯 Complete Example Workflows

### Example 1: Voice Note → Published Article

```python
from core.workflow_automation import ContentWorkflow

# Initialize workflow
workflow = ContentWorkflow("Max Bernstein")

# Process voice note
result = workflow.process_input(
    input_text="""
    So I was thinking about how AI is really changing the way we think 
    about expertise. You know, it used to be that expertise was about 
    knowing things, but now with AI, it's more about asking the right 
    questions. I mean, your brain lights up when it sees something new, 
    not just 'better' or 'improved' but actually new.
    """,
    input_type="voice_note",  # Auto-detected
    output_format="article",  # Auto-detected
    auto_humanize=True,
    auto_publish=True,
    publish_config={
        "destination": "wordpress",
        "site_url": "yoursite.com",
        "status": "draft"
    }
)

# Result:
# - Voice note processed and cleaned
# - Content generated with modular prompts
# - Humanized to remove AI-isms
# - Published to WordPress as draft
# - Returns: final_content, output_path, publish_result
```

**What Happens Behind the Scenes:**

1. **Input Detection:** Recognizes voice note patterns (filler words, conversational flow)
2. **Input Processing:** Removes "um", "you know", preserves energy
3. **Prompt Assembly:** Loads all modular files, assembles complete prompt
4. **Generation:** Claude generates article following Max's voice + structure
5. **Humanization:** Removes AI patterns, maintains voice
6. **Publishing:** Posts to WordPress as draft

---

### Example 2: Quick Topic → LinkedIn Post

```python
from core.workflow_automation import quick_content

# Ultra-simple workflow
content = quick_content(
    input_text="How AI reveals hidden expertise",
    profile_name="Max Bernstein"
)

# Result: Complete LinkedIn post, ready to publish
```

**What Happens:**

1. Auto-detects: Topic → LinkedIn (short input)
2. Loads modular prompts
3. Generates LinkedIn-optimized content
4. Humanizes automatically
5. Returns ready-to-publish content

---

### Example 3: API Request → Multi-Platform Content

```python
# Via API endpoint
POST /api/v1/content
{
  "input_text": "Your topic here",
  "input_type": "topic",
  "output_format": "article",
  "platforms": ["linkedin", "tiktok"],
  "auto_publish": true,
  "publish_config": {
    "destination": "github",
    "repo": "username/repo"
  }
}
```

**What Happens:**

1. API receives request
2. Workflow processes input
3. Modular prompts assembled
4. Platform optimization applied (LinkedIn + TikTok)
5. Content multiplication framework used
6. Generates article + LinkedIn post + TikTok script
7. Publishes to GitHub
8. Returns all variations

---

## 🔧 Component Details

### 1. Workflow Automation (`core/workflow_automation.py`)

**Purpose:** Orchestrates the complete pipeline

**Key Methods:**
- `process_input()` - Main entry point
- `_detect_input_type()` - Auto-detects input type
- `_detect_output_format()` - Auto-detects format
- `_process_voice_note()` - Cleans voice notes
- `_publish()` - Handles publishing

**Flow:**
```
Input → Detect Type → Process → Generate → Humanize → Publish → Return
```

---

### 2. Content Generator (`core/content_generator.py`)

**Purpose:** Generates content using AI

**Key Methods:**
- `generate()` - Main generation method
- `_create_modular_prompt()` - Assembles prompts
- `_generate_anthropic()` - Calls Claude API
- `_generate_openai()` - Calls OpenAI API

**Flow:**
```
Content Brief → Assemble Prompt → Call AI → Return Content
```

---

### 3. Prompt Assembler (`core/prompt_assembler.py`)

**Purpose:** Loads and assembles modular prompts

**Key Methods:**
- `load_file()` - Loads prompt file (with caching)
- `build_prompt()` - Assembles complete prompt
- `build_from_template()` - Uses assembly template

**Flow:**
```
Input Type → Load Relevant Files → Assemble → Return Complete Prompt
```

**Files Loaded:**
- Always: voice_profile, anti_ai, hook_engineering, content_structure, output_schema
- If viral: viral_psychology
- If platforms: platform_optimization, content_multiplication
- If input_type != topic: input_processing

---

### 4. Humanizer (`core/humanizer.py`)

**Purpose:** Removes AI-isms, maintains voice

**Key Methods:**
- `humanize()` - Main humanization method
- Uses Max's personalized humanizer prompt

**Flow:**
```
Generated Content → Scan for AI Patterns → Remove → Apply Voice → Return
```

---

### 5. Voice Profiler (`core/voice_profiler.py`)

**Purpose:** Manages voice profiles

**Key Methods:**
- `load_profile()` - Loads voice profile JSON
- `list_profiles()` - Lists available profiles

**Profile Structure:**
```json
{
  "metadata": {
    "name": "Max Bernstein",
    "created": "2025-01-01",
    "samples": {"count": 10}
  },
  "mechanics": {...},
  "style": {...},
  "strategy": {...}
}
```

---

## 📱 API Workflow

### Request Flow

```
Client Request
    ↓
FastAPI Server (api/server.py)
    ↓
ContentWorkflow.process_input()
    ↓
ContentGenerator.generate()
    ↓
PromptAssembler.build_prompt()
    ↓
AI Generation (Claude/GPT)
    ↓
Humanizer.humanize()
    ↓
Publisher.publish() (if enabled)
    ↓
JSON Response
```

### Endpoints

**Quick Content:**
```
POST /api/v1/quick
{
  "input_text": "Your topic"
}
→ Returns: Complete content, ready to publish
```

**Full Content:**
```
POST /api/v1/content
{
  "input_text": "Your topic",
  "input_type": "voice_note",
  "output_format": "article",
  "platforms": ["linkedin"],
  "auto_publish": true,
  "publish_config": {...}
}
→ Returns: Content + metadata + publish_result
```

**Voice Note:**
```
POST /api/v1/voice-note
{
  "transcript": "Your voice note transcript",
  "auto_publish": true
}
→ Returns: Processed content + publish_result
```

---

## 🎨 Modular Prompt System Flow

### File Loading

```
PromptAssembler.build_prompt()
    ↓
Load core/voice_profile_max.md
    ↓
Load core/anti_ai_patterns.md
    ↓
Load frameworks/hook_engineering.md
    ↓
Load frameworks/content_structure.md
    ↓
Load frameworks/viral_psychology.md (if include_viral)
    ↓
Load frameworks/platform_optimization.md (if platforms)
    ↓
Load frameworks/input_processing.md (if input_type != topic)
    ↓
Load core/output_schema.md
    ↓
Assemble into complete prompt
    ↓
Return to ContentGenerator
```

### Prompt Assembly Logic

```python
# Always loaded
- voice_profile_max.md
- anti_ai_patterns.md
- hook_engineering.md
- content_structure.md
- output_schema.md

# Conditionally loaded
- viral_psychology.md (if include_viral=True)
- platform_optimization.md (if platforms specified)
- content_multiplication.md (if multiple platforms)
- input_processing.md (if input_type != "topic")
```

---

## 🔍 Quality Verification Flow

### Pre-Generation Checks

```
1. Input type detected? ✓
2. Output format detected? ✓
3. Voice profile loaded? ✓
4. Modular prompts available? ✓
```

### Post-Generation Checks

```
1. Hook grabs in first 3 words? ✓
2. Zero banned AI patterns? ✓
3. Matches voice calibration? ✓
4. Specific numbers included? ✓
5. Story-first structure? ✓
6. List density 8-18? ✓
7. Paragraph average <10 words? ✓
```

### Quality Scores

```json
{
  "quality_scores": {
    "voice_match": 90,
    "hook_strength": 85,
    "list_density": 80,
    "specificity": 90,
    "ai_pattern_check": "pass",
    "banned_patterns_found": []
  }
}
```

---

## 🚀 Complete Workflow Examples

### Example A: CLI Quick Command

```bash
python3 cli/quick.py "How AI reveals hidden expertise"
```

**Flow:**
1. `quick.py` reads input
2. Calls `quick_content()` from workflow_automation
3. Workflow auto-detects: topic → article
4. ContentGenerator uses modular prompts
5. Generates content
6. Humanizes automatically
7. Prints result

**Time:** ~30-60 seconds

---

### Example B: API Quick Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "How AI reveals hidden expertise"}'
```

**Flow:**
1. FastAPI receives request
2. Calls `quick_content()`
3. Same workflow as CLI
4. Returns JSON response

**Time:** ~30-60 seconds

---

### Example C: Full Workflow with Publishing

```python
from core.workflow_automation import ContentWorkflow

workflow = ContentWorkflow("Max Bernstein")

result = workflow.process_input(
    input_text="Your voice note transcript",
    input_type="voice_note",
    output_format="article",
    target_length=2400,
    auto_humanize=True,
    auto_publish=True,
    publish_config={
        "destination": "wordpress",
        "site_url": "yoursite.com",
        "status": "draft"
    }
)
```

**Flow:**
1. Input processing (voice note cleaned)
2. Prompt assembly (modular files loaded)
3. Content generation (Claude with Max's voice)
4. Humanization (AI patterns removed)
5. Publishing (WordPress draft created)
6. Returns complete result

**Time:** ~60-90 seconds

---

## 📋 Input Type Handling

### Voice Note

**Detection:**
- Speech patterns (um, uh, like, you know)
- Conversational flow
- Longer text with filler words

**Processing:**
- Removes filler words
- Preserves energy and exact phrases
- Extracts story seeds
- Structures as content brief

**Prompt Loading:**
- Loads `input_processing.md` (voice note section)
- Applies energy mapping
- Extracts quotable phrases

---

### Transcript

**Detection:**
- Multiple speakers (Q&A format)
- Timestamps or speaker labels

**Processing:**
- Identifies key moments
- Extracts quotable sections
- Multi-angle extraction

**Prompt Loading:**
- Loads `input_processing.md` (transcript section)
- Speaker dynamics analysis
- Moment mining

---

### Topic

**Detection:**
- Default for everything else
- Short or long text without patterns

**Processing:**
- Used as-is
- No special processing

**Prompt Loading:**
- Standard prompt assembly
- No input_processing.md needed

---

## 🎯 Platform Optimization Flow

### When Platforms Specified

```python
config = GenerationConfig(
    platforms=["linkedin", "tiktok"]
)
```

**What Happens:**

1. Loads `platform_optimization.md`
2. Loads `content_multiplication.md`
3. Generates primary content
4. Creates platform variations:
   - LinkedIn: First line hook, professional angle
   - TikTok: 0-2 second hook, 30-60 sec script
5. Returns all variations

**Output Structure:**
```json
{
  "primary_content": {...},
  "variations": [
    {
      "platform": "linkedin",
      "adjusted_hook": "...",
      "structure_notes": "..."
    },
    {
      "platform": "tiktok",
      "adjusted_hook": "...",
      "structure_notes": "..."
    }
  ]
}
```

---

## 🔄 Error Handling & Fallbacks

### Prompt File Missing

```
If modular prompt file missing:
  → Falls back to default prompt
  → Logs warning
  → Continues generation
```

### API Key Missing

```
If API key missing:
  → Raises clear error
  → Suggests setting environment variable
  → Stops generation
```

### Voice Profile Missing

```
If voice profile missing:
  → Raises ValueError
  → Suggests creating profile
  → Stops generation
```

---

## 📊 Performance Metrics

### Typical Timings

- **Input Detection:** <1 second
- **Prompt Assembly:** 1-2 seconds
- **AI Generation:** 20-40 seconds
- **Humanization:** 10-20 seconds
- **Publishing:** 5-10 seconds

**Total:** 40-75 seconds for complete workflow

---

## 🎯 Key Integration Points

### 1. Workflow → Generator

```python
# Workflow calls generator
generation_result = self.generator.generate(
    content_brief=content_brief,
    voice_profile=self.voice_profile,
    config=config
)
```

### 2. Generator → Prompt Assembler

```python
# Generator calls assembler
assembler = PromptAssembler()
prompt = assembler.build_prompt(
    user_input=content_brief,
    input_type=config.input_type,
    platforms=config.platforms
)
```

### 3. Generator → Humanizer

```python
# Generator calls humanizer
humanize_result = self.humanizer.humanize(
    text=content,
    show_analysis=False
)
```

### 4. Workflow → Publisher

```python
# Workflow calls publisher
publish_result = self._publish(
    content=content,
    config=publish_config,
    format=output_format
)
```

---

## 🔍 Debugging Workflow

### Check Each Step

```python
# 1. Check input detection
workflow = ContentWorkflow("Max Bernstein")
input_type = workflow._detect_input_type("Your input")
print(f"Detected type: {input_type}")

# 2. Check prompt assembly
from core.prompt_assembler import PromptAssembler
assembler = PromptAssembler()
prompt = assembler.build_prompt("test", input_type="topic")
print(f"Prompt length: {len(prompt)}")

# 3. Check voice profile
from core.voice_profiler import VoiceProfiler
profiler = VoiceProfiler()
profile = profiler.load_profile("Max Bernstein")
print(f"Profile loaded: {profile['metadata']['name']}")

# 4. Check generation config
from core.content_generator import GenerationConfig
config = GenerationConfig(use_modular_prompts=True)
print(f"Modular prompts: {config.use_modular_prompts}")
```

---

## 📚 Related Documentation

- **Modular Prompts:** `MODULAR-PROMPTS-COMPLETE.md`
- **API Guide:** `api/README.md`
- **Workflow Automation:** `WORKFLOW-AUTOMATION.md`
- **Quick Start:** `QUICK-WORKFLOW-GUIDE.md`
- **End-to-End:** `END-TO-END-WORKFLOW.md`

---

## ✅ Summary

**Complete Flow:**
```
Input → Detect → Process → Assemble Prompts → Generate → Humanize → Publish → Done
```

**Key Components:**
1. **Workflow Automation** - Orchestrates everything
2. **Content Generator** - Generates with AI
3. **Prompt Assembler** - Loads modular prompts
4. **Humanizer** - Removes AI-isms
5. **Publisher** - Auto-publishes to platforms

**Everything works together automatically** - just provide input and get world-class content!

