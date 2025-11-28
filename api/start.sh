#!/bin/bash
# Start VoiceCraft API Server

cd "$(dirname "$0")/.."

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "⚠️  Warning: .env.local not found. API keys may not be loaded."
fi

# Start server
echo "🚀 Starting VoiceCraft API Server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📖 API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000

