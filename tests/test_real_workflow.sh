#!/bin/bash
# Test the workflow with real examples (requires API key)

set -e

# Change to project root
cd "$(dirname "$0")/.."

echo "🧪 Testing VoiceCraft Workflow"
echo "================================"
echo ""

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: No API key found"
    echo "Set ANTHROPIC_API_KEY or OPENAI_API_KEY to test full workflow"
    echo ""
    echo "Testing detection only..."
    python3 tests/test_workflow_detection.py
    exit 0
fi

echo "✅ API key found"
echo ""

# Test 1: Simple topic
echo "Test 1: Simple Topic"
echo "-------------------"
echo "Input: 'How AI is changing content creation'"
python3 cli/quick.py "How AI is changing content creation" > /tmp/test1_output.md 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Success - Output saved"
    echo "First 200 chars:"
    head -c 200 /tmp/test1_output.md
    echo ""
else
    echo "❌ Failed"
    cat /tmp/test1_output.md
fi
echo ""

# Test 2: Bullet points
echo "Test 2: Bullet Points"
echo "-------------------"
BULLETS="- Sales process is broken
- Need better training
- Communication issues
- Fix in 30 days"
echo "Input: Bullet points"
python3 cli/quick.py "$BULLETS" > /tmp/test2_output.md 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Success - Output saved"
    echo "First 200 chars:"
    head -c 200 /tmp/test2_output.md
    echo ""
else
    echo "❌ Failed"
    cat /tmp/test2_output.md
fi
echo ""

# Test 3: Short input (should be LinkedIn)
echo "Test 3: Short Input (LinkedIn)"
echo "-------------------"
echo "Input: 'Quick tip: Sales optimization'"
python3 cli/quick.py "Quick tip: Sales optimization" > /tmp/test3_output.md 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Success - Output saved"
    echo "First 200 chars:"
    head -c 200 /tmp/test3_output.md
    echo ""
else
    echo "❌ Failed"
    cat /tmp/test3_output.md
fi
echo ""

echo "================================"
echo "✅ All tests complete!"
echo "Check /tmp/test*_output.md for results"

