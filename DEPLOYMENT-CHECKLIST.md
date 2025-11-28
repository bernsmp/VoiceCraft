# Deployment Checklist

## ✅ Phase 1: CMS Sync Fix (COMPLETE)
- [x] Updated seed script to populate all default fields
- [x] Verified merge logic prioritizes CMS data
- [x] Tested CMS ↔ Site parity

## ✅ Phase 2: Slack Bot Integration (COMPLETE)
- [x] Fixed Slack response posting (uses WebClient)
- [x] Added confirmation flow with preview buttons
- [x] Enhanced error handling and logging
- [x] Added support for "add" commands (testimonials, FAQs, etc.)

## ✅ Phase 3: Railway Deployment Setup (COMPLETE)
- [x] Created `Procfile` for Railway
- [x] Created `railway.json` config
- [x] Added Flask to `requirements.txt`
- [x] Fixed signature verification for interactive endpoint
- [x] Created deployment documentation

## 🚀 Next Steps: Deploy to Railway

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Railway deployment files and Slack bot improvements"
git push
```

### 2. Create Railway Project
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `VoiceCraft` repository
4. Railway will auto-detect and deploy

### 3. Set Environment Variables in Railway
Go to Project → Variables tab, add:

**Required:**
- `SLACK_BOT_TOKEN` = `xoxb-your-bot-token-here`
- `SLACK_SIGNING_SECRET` = `your-signing-secret-here`
- `LOUIE_SITE_URL` = `https://louiebernstein.com`
- `LOUIE_ADMIN_EMAIL` = `your-admin-email@example.com`
- `LOUIE_ADMIN_PASSWORD` = `your-admin-password`
- `ANTHROPIC_API_KEY` = (your key)

**Optional:**
- `VERCEL_DEPLOY_HOOK_URL` = (if you want auto-deployments)
- `SLACK_DEPLOY_CHANNEL` = `#website-updates`

### 4. Get Railway URL
After deployment, Railway will provide a URL like:
```
https://your-app-name.railway.app
```

### 5. Update Slack App Configuration

#### Event Subscriptions
1. Go to https://api.slack.com/apps → Your App
2. Event Subscriptions → Enable Events
3. Request URL: `https://your-app-name.railway.app/slack/events`
4. Subscribe to:
   - `app_mentions`
   - `message.im`
5. Save

#### Slash Commands (Optional)
1. Slash Commands → Create `/site`
2. Request URL: `https://your-app-name.railway.app/slack/commands`
3. Save

### 6. Test the Bot
1. Send DM to bot: "Change headline to 'Test Headline'"
2. Should see preview with Confirm/Cancel buttons
3. Click Confirm → Change should apply
4. Check website to verify change

## 📋 Files Created/Modified

**New Files:**
- `Procfile` - Railway start command
- `railway.json` - Railway configuration
- `RAILWAY-DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT-CHECKLIST.md` - This file

**Modified Files:**
- `requirements.txt` - Added Flask
- `integrations/slack_bot_server.py` - Fixed posting, confirmation flow, signature verification
- `integrations/slack_bot.py` - Enhanced preview formatting, add command support

## 🔍 Testing Locally (Before Deploying)

```bash
# Set environment variables
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_SIGNING_SECRET="..."
export LOUIE_SITE_URL="https://louiebernstein.com"
export LOUIE_ADMIN_EMAIL="louis30092@gmail.com"
export LOUIE_ADMIN_PASSWORD="DoneGood#"
export ANTHROPIC_API_KEY="..."

# Install dependencies
pip install -r requirements.txt

# Run server
python3 integrations/slack_bot_server.py

# In another terminal, use ngrok
ngrok http 3001

# Update Slack app Request URL to ngrok URL
```

## 🐛 Troubleshooting

**Bot not responding:**
- Check Railway logs
- Verify environment variables
- Check Slack app Request URL matches Railway URL

**Signature verification failing:**
- Verify `SLACK_SIGNING_SECRET` is correct
- Check server is receiving requests (check logs)

**Import errors:**
- Ensure `requirements.txt` has all dependencies
- Railway installs via `pip install -r requirements.txt`

## 📚 Documentation

- Full deployment guide: `RAILWAY-DEPLOYMENT.md`
- Slack setup: `integrations/SLACK-CMS-SETUP.md`
- Slack commands: `integrations/SLACK-SETUP-GUIDE.md`

