# VoiceCraft Deployment Options

## 🎯 Where Can This Run?

VoiceCraft can run in multiple ways depending on your needs. Here are all the options:

---

## 🚀 Deployment Options

### 1. **Slack Bot** (Recommended for Team Use)

**How it works:**
- Slack bot listens for commands
- Processes requests via webhook
- Returns content directly in Slack
- Can auto-publish to your site

**Setup:**
```bash
# Install Slack SDK
pip install slack-sdk

# Set environment variables
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-secret"

# Run Slack bot
python3 integrations/slack_bot_server.py
```

**Usage in Slack:**
```
/content "How AI reveals hidden expertise"
→ Generates article, posts in Slack thread

/content-voice [paste transcript]
→ Processes voice note, returns content

/content-blend "topic" Hormozi:30
→ Generates with style blend
```

**Benefits:**
- ✅ Team collaboration
- ✅ Quick access from anywhere
- ✅ Thread-based organization
- ✅ Can trigger from mobile Slack app

**Best for:** Teams, agencies, collaborative content creation

---

### 2. **API Server** (Recommended for Production)

**How it works:**
- FastAPI server runs 24/7
- Accepts HTTP requests
- Can be deployed anywhere (VPS, cloud, etc.)
- Multiple clients can connect

**Setup:**
```bash
# Start server
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000

# Or use included script
./api/start.sh
```

**Deployment Options:**

**A. VPS (DigitalOcean, Linode, etc.)**
```bash
# Install on server
git clone your-repo
cd VoiceCraft
pip install -r requirements.txt

# Run with PM2 (keeps running)
pm2 start "uvicorn api.server:app --host 0.0.0.0 --port 8000" --name voicecraft-api

# Or systemd service
sudo systemctl start voicecraft-api
```

**B. Cloud Platforms**
- **Heroku:** `Procfile` with `web: uvicorn api.server:app --host 0.0.0.0 --port $PORT`
- **Railway:** Auto-detects FastAPI
- **Render:** Web service deployment
- **Fly.io:** Global edge deployment

**C. Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Usage:**
```bash
# From anywhere
curl -X POST https://your-server.com/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Your topic"}'
```

**Benefits:**
- ✅ Always available
- ✅ Scalable
- ✅ Multiple integrations possible
- ✅ Professional setup

**Best for:** Production use, multiple integrations, external services

---

### 3. **CLI Tool** (Local Development)

**How it works:**
- Runs on your local machine
- Command-line interface
- Fast for quick content

**Usage:**
```bash
# Quick content
python3 cli/quick.py "Your topic"

# Full workflow
python3 cli/voicecraft.py workflow create "Your topic" --publish
```

**Benefits:**
- ✅ Fast
- ✅ No server needed
- ✅ Good for testing
- ✅ Works offline (after setup)

**Best for:** Personal use, development, testing

---

### 4. **Web Dashboard** (Planned)

**How it works:**
- Next.js frontend
- Connects to API server
- Visual interface
- Content management

**Status:** Not built yet (in roadmap)

**Benefits:**
- ✅ Visual interface
- ✅ Content library
- ✅ Analytics dashboard
- ✅ Team collaboration

**Best for:** Non-technical users, content teams

---

### 5. **Mobile App** (Future)

**How it works:**
- React Native app
- Connects to API
- Voice note recording
- Quick content creation

**Status:** Not built yet (in roadmap)

**Benefits:**
- ✅ On-the-go access
- ✅ Voice note recording
- ✅ Push notifications
- ✅ Native mobile experience

**Best for:** Mobile-first workflows, voice notes

---

### 6. **Email Integration** (Structure Ready)

**How it works:**
- Email server receives emails
- Processes via workflow
- Replies with content

**Setup:**
```python
# Email trigger (structure exists)
from integrations.email_trigger import EmailContentTrigger

trigger = EmailContentTrigger()
result = trigger.process_email(
    subject="[CONTENT] Your topic",
    body="Details here",
    from_email="user@example.com"
)
```

**Benefits:**
- ✅ Email-based workflow
- ✅ No app needed
- ✅ Works from any email client

**Best for:** Email-first workflows, non-technical users

---

## 🎯 Recommended Setup

### For Personal Use
**Option:** CLI + API Server (local)
- Run API server locally
- Use CLI for quick content
- Use API for integrations

### For Team Use
**Option:** Slack Bot + API Server
- Deploy API server (VPS/cloud)
- Connect Slack bot to API
- Team uses Slack commands

### For Production/Client Use
**Option:** API Server + Web Dashboard
- Deploy API server (cloud)
- Build web dashboard
- Clients access via web

### For Mobile-First
**Option:** API Server + Mobile App
- Deploy API server (cloud)
- Build mobile app
- Connect app to API

---

## 🔧 Slack Integration Deep Dive

### Architecture

```
Slack → Slack Bot Server → VoiceCraft API → Content → Slack
```

**Components:**

1. **Slack Bot Server** (`integrations/slack_bot_server.py`)
   - Listens for Slack events
   - Processes commands
   - Calls VoiceCraft API
   - Returns formatted responses

2. **VoiceCraft API** (`api/server.py`)
   - Handles content generation
   - Processes all workflows
   - Returns structured content

3. **Slack Webhook**
   - Receives Slack events
   - Validates requests
   - Triggers bot logic

### Slack Bot Setup

**Step 1: Create Slack App**
1. Go to https://api.slack.com/apps
2. Create new app
3. Add bot token scopes: `chat:write`, `commands`
4. Install to workspace

**Step 2: Set Up Webhook**
1. Enable Events API
2. Add event subscriptions
3. Set request URL (your server)
4. Subscribe to: `app_mentions`, `message.channels`

**Step 3: Deploy Bot Server**
```python
# integrations/slack_bot_server.py
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from api.server import app  # Your API server

slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

@app.post("/slack/events")
async def slack_events(request: Request):
    # Handle Slack events
    # Call VoiceCraft API
    # Return formatted response
```

**Step 4: Commands**

```
/content "How AI reveals hidden expertise"
→ Generates article, posts in thread

/content-voice [transcript]
→ Processes voice note

/content-blend "topic" Hormozi:30
→ Style blend generation
```

### Slack Bot Features

**Current (Structure Ready):**
- `/content` - Generate from topic
- `/content-voice` - Process voice note
- `/content-blend` - Style fusion

**Could Add:**
- `/content-list` - Show recent content
- `/content-publish` - Publish to site
- `/content-stats` - Show performance
- `/content-help` - Show commands

---

## 🌐 Deployment Architecture

### Option A: Single Server

```
┌─────────────────────────────────┐
│         Your Server              │
│  ┌──────────┐  ┌─────────────┐  │
│  │ Slack Bot│  │  API Server │  │
│  │  Server  │→ │  (FastAPI)  │  │
│  └──────────┘  └─────────────┘  │
│         │              │         │
└─────────┼──────────────┼─────────┘
          │              │
    ┌─────┘              └─────┐
    │                          │
┌───▼───┐              ┌──────▼─────┐
│ Slack │              │  External   │
│       │              │  Clients    │
└───────┘              └─────────────┘
```

### Option B: Separate Services

```
┌─────────────┐
│ Slack Bot   │ → API Server (Cloud)
│ (Local/VPS) │
└─────────────┘

┌─────────────┐
│ API Server  │ ← Mobile App, Web Dashboard, etc.
│  (Cloud)    │
└─────────────┘
```

---

## 💡 Recommended: Slack + API Server

**Why this combo:**

1. **Slack Bot** - Easy team access
   - Commands from Slack
   - Thread-based organization
   - Mobile Slack app works

2. **API Server** - Flexible backend
   - Can add more integrations later
   - Web dashboard can connect
   - Mobile app can connect
   - Zapier/Make.com can connect

**Setup:**

```bash
# 1. Deploy API server (VPS/cloud)
# 2. Set up Slack bot pointing to API
# 3. Team uses Slack commands
# 4. Future: Add web dashboard, mobile app, etc.
```

---

## 🚀 Quick Start: Slack Bot

**I can build the complete Slack bot server for you:**

1. **Slack Bot Server** (`integrations/slack_bot_server.py`)
   - Handles Slack events
   - Processes commands
   - Calls VoiceCraft API
   - Returns formatted responses

2. **Slack Commands**
   - `/content` - Quick generation
   - `/content-voice` - Voice note processing
   - `/content-publish` - Auto-publish

3. **Deployment Guide**
   - Slack app setup
   - Webhook configuration
   - Server deployment

**Want me to build the complete Slack integration?**

---

## 📊 Comparison Table

| Option | Setup Complexity | Best For | Scalability |
|--------|-----------------|----------|-------------|
| **CLI** | ⭐ Easy | Personal use | Low |
| **API Server** | ⭐⭐ Medium | Production | High |
| **Slack Bot** | ⭐⭐⭐ Medium | Teams | Medium |
| **Web Dashboard** | ⭐⭐⭐⭐ Hard | Non-technical | High |
| **Mobile App** | ⭐⭐⭐⭐⭐ Very Hard | Mobile-first | High |

---

## 🎯 My Recommendation

**Start with:** API Server + Slack Bot

**Why:**
- ✅ API server = flexible foundation
- ✅ Slack bot = easy team access
- ✅ Can add more later (web, mobile)
- ✅ Professional setup

**Deploy:**
1. API server on VPS/cloud (Railway, Render, Fly.io)
2. Slack bot connects to API
3. Team uses Slack commands
4. Future: Add web dashboard, mobile app

---

**Want me to build the complete Slack bot integration?** I can create:
- Slack bot server
- Command handlers
- Deployment guide
- Setup instructions

