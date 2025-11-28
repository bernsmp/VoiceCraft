#!/bin/bash
# Test VoiceCraft API endpoints

API_URL="http://localhost:8000"

echo "🧪 Testing VoiceCraft API"
echo "=========================="
echo ""

# Test health check
echo "1. Testing health check..."
curl -s "$API_URL/health" | python3 -m json.tool
echo ""
echo ""

# Test quick content
echo "2. Testing quick content endpoint..."
curl -s -X POST "$API_URL/api/v1/quick" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI is changing expertise"
  }' | python3 -m json.tool | head -20
echo ""
echo ""

# Test profiles
echo "3. Testing profiles endpoint..."
curl -s "$API_URL/api/v1/profiles" | python3 -m json.tool
echo ""
echo ""

echo "✅ Tests complete!"
echo ""
echo "Full API docs: $API_URL/docs"

