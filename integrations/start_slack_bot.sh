#!/bin/bash
# Quick start script for Slack Bot Server

echo "🚀 Starting VoiceCraft Slack Bot Server..."
echo ""

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found!"
    echo "Creating template..."
    cat > .env.local << EOF
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
VOICECRAFT_PROFILE=Max Bernstein
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
EOF
    echo "✅ Created .env.local template"
    echo "⚠️  Please edit .env.local with your actual tokens!"
    exit 1
fi

# Check if slack-sdk is installed
if ! python3 -c "import slack_sdk" 2>/dev/null; then
    echo "📦 Installing slack-sdk..."
    pip install slack-sdk
fi

# Check environment variables
if [ -z "$SLACK_BOT_TOKEN" ] && ! grep -q "SLACK_BOT_TOKEN" .env.local 2>/dev/null; then
    echo "⚠️  SLACK_BOT_TOKEN not set!"
    echo "Please set it in .env.local or as environment variable"
    exit 1
fi

# Start the server
echo "✅ Starting bot server on port 3000..."
echo "📍 Endpoints:"
echo "   - POST /slack/events (Events API)"
echo "   - POST /slack/commands (Slash Commands)"
echo "   - GET /slack/health (Health check)"
echo ""
echo "💡 For local testing, use ngrok:"
echo "   ngrok http 3000"
echo "   Then update Slack app Request URL to ngrok URL"
echo ""

python3 integrations/slack_bot_server.py

