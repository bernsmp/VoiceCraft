# Quick Deploy Guide

## 🚀 Deploy to Railway in 5 Steps

### Step 1: Initialize Git (if not already done)
```bash
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"
git init
git add .
git commit -m "Add Slack bot integration and Railway deployment files"
```

### Step 2: Push to GitHub
```bash
# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/VoiceCraft.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Railway
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect GitHub (if needed)
5. Select **VoiceCraft** repository
6. Railway will auto-detect and start deploying

### Step 4: Set Environment Variables
In Railway dashboard → Your Project → **Variables** tab:

Click **"New Variable"** and add each:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

```
SLACK_SIGNING_SECRET=your-signing-secret-here
```

```
LOUIE_SITE_URL=https://louiebernstein.com
```

```
LOUIE_ADMIN_EMAIL=your-admin-email@example.com
```

```
LOUIE_ADMIN_PASSWORD=your-admin-password
```

```
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

**Optional:**
```
VERCEL_DEPLOY_HOOK_URL=your-vercel-deploy-hook-url
SLACK_DEPLOY_CHANNEL=#website-updates
```

### Step 5: Update Slack App

After Railway deploys (usually 1-2 minutes), you'll get a URL like:
```
https://your-app-name.railway.app
```

#### Update Event Subscriptions:
1. Go to https://api.slack.com/apps → Your Slack App
2. **Event Subscriptions** → Toggle **"Enable Events"** ON
3. **Request URL**: `https://your-app-name.railway.app/slack/events`
4. Slack will verify (should auto-verify ✅)
5. Under **"Subscribe to bot events"**, add:
   - `app_mentions`
   - `message.im`
6. Click **"Save Changes"**

#### Update Slash Commands (Optional):
1. **Slash Commands** → **"Create New Command"**
2. Command: `/site`
3. Request URL: `https://your-app-name.railway.app/slack/commands`
4. Description: "Edit website content"
5. Usage hint: "Change headline to 'New Headline'"
6. Click **"Save"**

### Step 6: Test! 🎉

1. In Slack, send a DM to your bot
2. Try: **"Change headline to 'Test Headline'"**
3. Bot should respond with preview + Confirm/Cancel buttons
4. Click **"Confirm"** → Change applies!
5. Check https://louiebernstein.com to verify

## ✅ What's Ready

- ✅ Slack bot server with Flask
- ✅ Response posting (not just prints)
- ✅ Preview + confirmation flow
- ✅ Signature verification
- ✅ Error handling
- ✅ Support for "add" commands
- ✅ Railway deployment files (Procfile, railway.json)
- ✅ Health check endpoint

## 📋 Files Created

- `Procfile` - Railway start command
- `railway.json` - Railway config
- `RAILWAY-DEPLOYMENT.md` - Detailed guide
- `DEPLOYMENT-CHECKLIST.md` - Checklist
- `QUICK-DEPLOY.md` - This file

## 🐛 Troubleshooting

**Bot not responding?**
- Check Railway logs: Project → Deployments → Click deployment → Logs
- Verify all environment variables are set
- Check Slack app Request URL matches Railway URL exactly

**Signature verification failing?**
- Double-check `SLACK_SIGNING_SECRET` matches Slack app
- Verify server is running (check Railway logs)

**Import errors?**
- Check `requirements.txt` has all dependencies
- Railway installs via `pip install -r requirements.txt`

## 📞 Need Help?

Check the detailed guides:
- `RAILWAY-DEPLOYMENT.md` - Full deployment guide
- `DEPLOYMENT-CHECKLIST.md` - Step-by-step checklist

