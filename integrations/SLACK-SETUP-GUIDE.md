# Slack Bot Setup Guide

## 🎯 Complete Slack Integration

This guide shows you how to set up VoiceCraft as a Slack bot so your team can generate content directly from Slack.

---

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install slack-sdk
```

### Step 2: Create Slack App

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "VoiceCraft" (or your choice)
4. Workspace: Select your workspace
5. Click "Create App"

### Step 3: Configure Bot Token Scopes

1. Go to "OAuth & Permissions" in sidebar
2. Scroll to "Scopes"
3. Add Bot Token Scopes:
   - `chat:write` - Post messages
   - `commands` - Handle slash commands
   - `app_mentions:read` - Respond to mentions
   - `channels:read` - Read channel info

### Step 4: Install App to Workspace

1. Scroll to top of "OAuth & Permissions"
2. Click "Install to Workspace"
3. Authorize the app
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### Step 5: Set Up Slash Commands

1. Go to "Slash Commands" in sidebar
2. Click "Create New Command"
3. Command: `/content`
   - Request URL: `https://your-server.com/slack/commands`
   - Short description: "Generate content with VoiceCraft"
   - Usage hint: "Your topic here"
4. Create another command: `/content-voice`
   - Request URL: `https://your-server.com/slack/commands`
   - Short description: "Process voice note transcript"
   - Usage hint: "[paste transcript]"

### Step 6: Set Up Events API (Optional - for @mentions)

1. Go to "Event Subscriptions" in sidebar
2. Enable Events
3. Request URL: `https://your-server.com/slack/events`
4. Subscribe to bot events:
   - `app_mentions` - When bot is mentioned
5. Save changes

### Step 7: Get Signing Secret

1. Go to "Basic Information" in sidebar
2. Under "App Credentials"
3. Copy "Signing Secret"

### Step 8: Set Environment Variables

```bash
export SLACK_BOT_TOKEN="xoxb-your-token-here"
export SLACK_SIGNING_SECRET="your-signing-secret-here"
export VOICECRAFT_PROFILE="Max Bernstein"
```

Or add to `.env.local`:
```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
VOICECRAFT_PROFILE=Max Bernstein
```

### Step 9: Deploy Bot Server

**Option A: Run Locally (Testing)**
```bash
python3 integrations/slack_bot_server.py
```

**Option B: Deploy to Server**
```bash
# On your server
cd VoiceCraft
pip install slack-sdk
python3 integrations/slack_bot_server.py

# Or with PM2
pm2 start "python3 integrations/slack_bot_server.py" --name voicecraft-slack

# Or with systemd
sudo systemctl start voicecraft-slack
```

**Option C: Deploy with API Server**
```bash
# Run both together
uvicorn api.server:app --host 0.0.0.0 --port 8000 &
python3 integrations/slack_bot_server.py --port 3000
```

### Step 10: Test in Slack

In any Slack channel:
```
/content How AI reveals hidden expertise
```

Bot should respond with generated content!

---

## 📱 Available Commands

### `/content [topic]`
Generate content from a topic.

**Example:**
```
/content How AI reveals hidden expertise
```

**Response:** Full article in thread

---

### `/content-voice [transcript]`
Process a voice note transcript.

**Example:**
```
/content-voice So I was thinking about how AI is changing expertise. You know, it used to be that expertise was about knowing things, but now...
```

**Response:** Processed and formatted content

---

### `/content-help`
Show help message.

**Response:** List of available commands

---

## 🔧 Architecture

```
Slack → Slack Bot Server → VoiceCraft API → Content → Slack Response
```

**Flow:**
1. User types `/content topic` in Slack
2. Slack sends request to your server (`/slack/commands`)
3. Bot server processes command
4. Calls VoiceCraft workflow
5. Generates content
6. Returns formatted response to Slack

---

## 🌐 Deployment Options

### Option 1: Same Server as API

Run both on same server:
```bash
# API server (port 8000)
uvicorn api.server:app --host 0.0.0.0 --port 8000

# Slack bot (port 3000)
python3 integrations/slack_bot_server.py
```

### Option 2: Separate Servers

- API server: Cloud/VPS (always on)
- Slack bot: Can run anywhere (connects to API)

### Option 3: Serverless (Future)

- API: Serverless function
- Slack bot: Serverless function
- Both triggered on demand

---

## 🔐 Security

### Request Verification

The bot verifies all Slack requests using the signing secret:

```python
# Automatically verifies:
# - Request timestamp (prevents replay attacks)
# - Request signature (HMAC SHA256)
# - Returns 401 if invalid
```

### Token Security

- Never commit tokens to git
- Use environment variables
- Rotate tokens if compromised
- Use different tokens per environment

---

## 🐛 Troubleshooting

### Bot Not Responding

1. **Check token:**
   ```bash
   echo $SLACK_BOT_TOKEN
   ```

2. **Check server is running:**
   ```bash
   curl http://localhost:3000/slack/health
   ```

3. **Check Slack app settings:**
   - Request URL correct?
   - Commands enabled?
   - Bot installed to workspace?

### "Invalid signature" Error

- Check `SLACK_SIGNING_SECRET` is set correctly
- Verify request URL matches Slack app settings
- Check server time is synced (for timestamp validation)

### "Missing scope" Error

- Add required scopes in Slack app settings
- Reinstall app to workspace after adding scopes

---

## 🎯 Advanced Features (Future)

### Auto-Publish to Site

```
/content-publish "topic" --site yoursite.com
```

### Content Library

```
/content-list
/content-show [id]
```

### Analytics

```
/content-stats
```

### Team Collaboration

- Assign content to team members
- Review workflow
- Approval process

---

## 📊 Usage Examples

### Quick Content Generation

```
User: /content How AI reveals hidden expertise

Bot: [Generates article, posts in thread]
```

### Voice Note Processing

```
User: /content-voice [pastes transcript]

Bot: [Processes, cleans, generates content]
```

### Help

```
User: /content-help

Bot: [Shows available commands]
```

---

## ✅ Setup Checklist

- [ ] Slack app created
- [ ] Bot token scopes added
- [ ] App installed to workspace
- [ ] Slash commands configured
- [ ] Events API configured (optional)
- [ ] Signing secret copied
- [ ] Environment variables set
- [ ] Bot server deployed
- [ ] Tested in Slack

---

## 🚀 Next Steps

1. **Set up Slack app** (follow steps above)
2. **Deploy bot server** (your server or cloud)
3. **Test commands** in Slack
4. **Share with team** - they can now generate content from Slack!

---

**The Slack bot is ready to use!** Your team can generate content directly from Slack without leaving the app.

