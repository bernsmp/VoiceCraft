# Slack Bot Mobile Quick Start 📱

## 🎯 Perfect for Mobile Use!

Generate content from your phone using Slack - it's that simple!

---

## ⚡ 3-Step Setup

### 1. Create Slack App (5 min)
- Go to https://api.slack.com/apps
- Create app → Install → Copy token

### 2. Deploy Bot Server (5 min)
```bash
./integrations/start_slack_bot.sh
```

### 3. Use on Your Phone! 📱
```
/content Your topic here
```

---

## 📱 Mobile Commands

**Quick Content:**
```
/content How AI reveals hidden expertise
```

**Voice Note:**
```
/content-voice [paste transcript]
```

**Help:**
```
/content-help
```

---

## 🚀 Deploy Options

### Local Testing (with ngrok)
```bash
# Terminal 1: Start bot
./integrations/start_slack_bot.sh

# Terminal 2: Expose with ngrok
ngrok http 3000

# Copy ngrok URL → Update Slack app Request URL
```

### Production (Railway/Render)
1. Deploy `slack_bot_server.py`
2. Set environment variables
3. Update Slack app Request URL
4. Done!

---

## ✅ That's It!

**Now use from your phone:**
1. Open Slack mobile app
2. Type `/content [topic]`
3. Get content instantly!

**See `MOBILE-SLACK-SETUP.md` for full details!**

