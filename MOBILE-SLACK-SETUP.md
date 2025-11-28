# Mobile Slack Setup - Quick Start 🚀

## 🎯 Perfect for Mobile Use!

Slack Bot works **perfectly on your phone** - you can generate content from anywhere using the Slack mobile app.

---

## ✅ Why Slack Bot is Perfect for Mobile

- ✅ **Slack mobile app** - Works on iOS and Android
- ✅ **Voice notes** - Record voice notes directly in Slack
- ✅ **Quick commands** - Type `/content` and go
- ✅ **Thread replies** - Content appears in organized threads
- ✅ **Works offline** - Queue commands, syncs when online
- ✅ **Notifications** - Get notified when content is ready

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Slack App

1. Go to https://api.slack.com/apps (on your computer)
2. Click **"Create New App"** → **"From scratch"**
3. Name: **"VoiceCraft"**
4. Workspace: Select your workspace
5. Click **"Create App"**

### Step 2: Add Bot Token Scopes

1. In sidebar: **"OAuth & Permissions"**
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Click **"Add an OAuth Scope"** and add:
   - `chat:write` - Post messages
   - `commands` - Handle slash commands
   - `app_mentions:read` - Respond to mentions

### Step 3: Install App

1. Scroll to top of **"OAuth & Permissions"**
2. Click **"Install to Workspace"**
3. Authorize
4. **Copy the Bot Token** (starts with `xoxb-`)

### Step 4: Create Slash Commands

**Command 1: `/content`**
1. Sidebar: **"Slash Commands"**
2. Click **"Create New Command"**
3. Fill in:
   - **Command:** `/content`
   - **Request URL:** `https://your-server.com/slack/commands`
   - **Short Description:** `Generate content with VoiceCraft`
   - **Usage Hint:** `Your topic here`
4. Click **"Save"**

**Command 2: `/content-voice`**
1. Click **"Create New Command"** again
2. Fill in:
   - **Command:** `/content-voice`
   - **Request URL:** `https://your-server.com/slack/commands`
   - **Short Description:** `Process voice note transcript`
   - **Usage Hint:** `[paste transcript]`
3. Click **"Save"**

### Step 5: Get Signing Secret

1. Sidebar: **"Basic Information"**
2. Under **"App Credentials"**
3. Copy **"Signing Secret"**

### Step 6: Set Environment Variables

On your server, create/update `.env.local`:

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
VOICECRAFT_PROFILE=Max Bernstein
```

### Step 7: Deploy Bot Server

**Option A: Same Server as API**
```bash
# If API is already running on port 8000
python3 integrations/slack_bot_server.py
# Bot runs on port 3000
```

**Option B: Deploy to Cloud**
```bash
# On Railway/Render/Fly.io
# Set environment variables in dashboard
# Deploy slack_bot_server.py
```

**Option C: Run Locally (Testing)**
```bash
python3 integrations/slack_bot_server.py
# Use ngrok to expose: ngrok http 3000
# Update Slack app Request URL to ngrok URL
```

### Step 8: Test on Your Phone! 📱

1. Open **Slack mobile app**
2. Go to any channel
3. Type: `/content How AI reveals hidden expertise`
4. Send!
5. Bot responds with generated content!

---

## 📱 Mobile Usage Tips

### Quick Content Generation

**In Slack mobile app:**
```
/content Your topic here
```

**Bot responds in thread with:**
- Generated content
- Formatted nicely
- Ready to copy/paste

### Voice Note Processing

**Option 1: Record in Slack**
1. Record voice note in Slack
2. Copy transcript (if auto-transcribed)
3. Type: `/content-voice [paste transcript]`

**Option 2: External Voice Note**
1. Record voice note elsewhere (Otter.ai, etc.)
2. Copy transcript
3. Type: `/content-voice [paste transcript]`

### Quick Commands

```
/content-help          → Show all commands
/content [topic]       → Generate content
/content-voice [text]  → Process voice note
```

---

## 🎯 Mobile Workflow Examples

### Example 1: Quick Idea → Content

**On your phone:**
1. Have an idea while walking
2. Open Slack mobile app
3. Type: `/content How AI reveals hidden expertise`
4. Send
5. Get notification when content is ready
6. Copy content, use anywhere!

### Example 2: Voice Note → Article

**On your phone:**
1. Record voice note (in Slack or elsewhere)
2. Copy transcript
3. Type: `/content-voice [paste transcript]`
4. Send
5. Get full article back!

### Example 3: Team Collaboration

**Team workflow:**
1. Someone shares idea in Slack channel
2. You: `/content [idea]`
3. Bot generates content
4. Team sees it in thread
5. Everyone can collaborate!

---

## 🔧 Server Setup Options

### Option 1: Deploy to Railway (Easiest)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select VoiceCraft repo
4. Set environment variables:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `VOICECRAFT_PROFILE`
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
5. Deploy!
6. Get URL: `https://your-app.railway.app`
7. Update Slack app Request URL

### Option 2: Deploy to Render

1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python3 integrations/slack_bot_server.py`
6. Set environment variables
7. Deploy!

### Option 3: VPS (DigitalOcean, Linode)

```bash
# SSH into server
git clone your-repo
cd VoiceCraft
pip install -r requirements.txt

# Set environment variables
nano .env.local

# Run with PM2 (keeps running)
pm2 start "python3 integrations/slack_bot_server.py" --name voicecraft-slack
pm2 save
pm2 startup
```

---

## 🎨 Mobile-Optimized Features

### Thread-Based Organization

All content appears in **threads**, so:
- ✅ Easy to find later
- ✅ Doesn't clutter channel
- ✅ Organized by conversation

### Rich Formatting

Bot responses use Slack's **rich blocks**:
- ✅ Formatted text
- ✅ Code blocks for full content
- ✅ Easy to copy/paste

### Notifications

Get notified when:
- ✅ Content is ready
- ✅ Processing starts
- ✅ Errors occur

---

## 🐛 Troubleshooting Mobile

### Bot Not Responding on Phone

1. **Check bot is running:**
   ```bash
   curl https://your-server.com/slack/health
   ```

2. **Check Slack app settings:**
   - Request URL correct?
   - Commands enabled?
   - Bot installed to workspace?

3. **Check mobile Slack app:**
   - App updated?
   - Workspace synced?
   - Try restarting app

### Commands Not Showing

1. **Reinstall Slack app:**
   - Uninstall app from workspace
   - Reinstall
   - Commands should appear

2. **Check command permissions:**
   - Make sure bot has `commands` scope
   - Reinstall after adding scopes

### Content Not Generating

1. **Check API keys:**
   ```bash
   echo $ANTHROPIC_API_KEY
   echo $OPENAI_API_KEY
   ```

2. **Check server logs:**
   ```bash
   # If using PM2
   pm2 logs voicecraft-slack
   ```

---

## ✅ Setup Checklist

- [ ] Slack app created
- [ ] Bot token scopes added
- [ ] App installed to workspace
- [ ] Slash commands created (`/content`, `/content-voice`)
- [ ] Signing secret copied
- [ ] Environment variables set
- [ ] Bot server deployed
- [ ] Request URLs updated in Slack app
- [ ] Tested on computer
- [ ] **Tested on phone!** 📱

---

## 🚀 You're Ready!

**Now you can:**
- ✅ Generate content from your phone
- ✅ Use voice notes anywhere
- ✅ Quick commands in Slack
- ✅ Get content instantly

**Try it now:**
1. Open Slack mobile app
2. Type: `/content Test topic`
3. Send!
4. See content appear! 🎉

---

## 📞 Need Help?

- **Slack app setup:** https://api.slack.com/apps
- **Bot server code:** `integrations/slack_bot_server.py`
- **Full guide:** `integrations/SLACK-SETUP-GUIDE.md`

**The bot is ready - just deploy and use from your phone!** 📱✨

