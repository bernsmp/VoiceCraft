# Workflow Test Results

## Auto-Detection Tests

Run `python3 test_workflow_detection.py` to test detection logic without API keys.

## Full Workflow Test (Requires API Key)

### Setup

1. **Set API Key:**
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   # or
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Set Profile (optional):**
   ```bash
   export VOICECRAFT_PROFILE="Max Bernstein"
   ```

### Test Commands

#### Test 1: Simple Topic
```bash
python3 cli/quick.py "How AI is changing content creation"
```

**Expected:**
- Input type: `topic`
- Output format: `article`
- Generates full article
- Saves to `data/outputs/workflow/`

#### Test 2: Bullet Points
```bash
python3 cli/quick.py "- Sales process is broken
- Need better training  
- Communication issues
- Fix in 30 days"
```

**Expected:**
- Input type: `bullet_points`
- Output format: `article`
- Converts bullets to narrative
- Generates article

#### Test 3: Voice Note Transcript
```bash
python3 cli/quick.py "So I was thinking about this problem where sales teams are struggling with... um... you know, the whole process is broken and we need to fix it but like, how do we do that?"
```

**Expected:**
- Input type: `voice_note`
- Output format: `article`
- Cleans filler words
- Generates article

#### Test 4: WhatsApp Paste
```bash
python3 cli/quick.py "[11:23 AM] You: Hey, I have an idea
[11:24 AM] Me: What's that?
[11:25 AM] You: We should write about sales optimization"
```

**Expected:**
- Input type: `whatsapp`
- Output format: `article`
- Extracts content from conversation
- Generates article

#### Test 5: Short Input (LinkedIn)
```bash
python3 cli/quick.py "Quick tip: Sales optimization"
```

**Expected:**
- Input type: `topic`
- Output format: `linkedin` (auto-detected from length)
- Generates LinkedIn post

#### Test 6: Explicit Format Request
```bash
python3 cli/quick.py "Write a twitter thread about AI content creation"
```

**Expected:**
- Input type: `topic`
- Output format: `twitter` (detected from keyword)
- Generates Twitter thread

### Test Workflow Command

```bash
# Quick workflow
python3 cli/workflow.py quick "Your topic here"

# Full workflow with options
python3 cli/workflow.py create "Your topic" --profile "Max Bernstein"
```

## Expected Output

All tests should:
1. ✅ Auto-detect input type
2. ✅ Auto-detect output format
3. ✅ Generate content silently (no prompts)
4. ✅ Save to `data/outputs/workflow/`
5. ✅ Print file path to stdout

## Troubleshooting

### "API key not found"
```bash
export ANTHROPIC_API_KEY="your-key"
# or
export OPENAI_API_KEY="your-key"
```

### "Profile not found"
```bash
# Check available profiles
python3 cli/voicecraft.py profile list

# Create profile if needed
python3 cli/voicecraft.py profile create --name "Max Bernstein" --samples "./data/samples/*.md"
```

### "Module not found"
```bash
pip3 install -r requirements.txt
```

## Success Criteria

✅ Auto-detection works for all input types  
✅ No prompts or confirmations  
✅ Content generated successfully  
✅ File saved correctly  
✅ Output is humanized and ready to publish

