# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account (if not already connected)
5. Select the `VoiceCraft` repository
6. Railway will auto-detect the project

### Step 2: Configure Environment Variables

In Railway dashboard, go to your project → Variables tab, and add:

```bash
# Slack Bot Credentials (REQUIRED)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

# Louie's Website CMS (REQUIRED)
LOUIE_SITE_URL=https://louiebernstein.com
LOUIE_ADMIN_EMAIL=your-admin-email@example.com
LOUIE_ADMIN_PASSWORD=your-admin-password

# LLM Parsing (REQUIRED for natural language commands)
ANTHROPIC_API_KEY=your-anthropic-key-here

# Optional: Deploy webhooks
VERCEL_DEPLOY_HOOK_URL=your-vercel-deploy-hook-url
SLACK_DEPLOY_CHANNEL=#website-updates

# Port (Railway sets this automatically, but you can override)
PORT=3001
```

### Step 3: Deploy

Railway will automatically:
1. Detect the `Procfile` and use it to start the server
2. Install dependencies from `requirements.txt`
3. Run `python3 integrations/slack_bot_server.py`
4. Expose the app on a public URL (e.g., `https://your-app.railway.app`)

### Step 4: Update Slack App Configuration

After Railway deploys, you'll get a public URL like:
```
https://your-app-name.railway.app
```

#### Update Event Subscriptions

1. Go to https://api.slack.com/apps → Your Slack App
2. Go to "Event Subscriptions" in sidebar
3. Enable Events (toggle ON)
4. Set Request URL to: `https://your-app-name.railway.app/slack/events`
5. Slack will verify the URL (should auto-verify if server is running)
6. Subscribe to bot events:
   - `app_mentions` - When bot is mentioned
   - `message.im` - Direct messages to bot
7. Click "Save Changes"

#### Update Slash Commands (Optional)

1. Go to "Slash Commands" in sidebar
2. Create command: `/site`
3. Request URL: `https://your-app-name.railway.app/slack/commands`
4. Description: "Edit website content"
5. Usage hint: "Change headline to 'New Headline'"
6. Save

### Step 5: Test the Bot

1. In Slack, send a DM to your bot or mention it in a channel
2. Try: "Change headline to 'Test Headline'"
3. Bot should respond with a preview and confirmation buttons
4. Click "Confirm" to apply the change

## Health Check

Railway will automatically check:
- `GET /` - Should return `{"status": "healthy", ...}`

## Troubleshooting

### Bot Not Responding

1. Check Railway logs: Project → Deployments → Click deployment → View logs
2. Verify environment variables are set correctly
3. Check Slack app Request URL matches Railway URL
4. Verify Slack app is installed to workspace

### URL Verification Failing

1. Make sure server is running (check Railway logs)
2. Verify `/slack/events` endpoint returns challenge correctly
3. Check `SLACK_SIGNING_SECRET` is set correctly

### Import Errors

1. Check `requirements.txt` includes all dependencies
2. Railway uses `pip install -r requirements.txt`
3. If missing dependencies, add them to `requirements.txt`

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot User OAuth Token from Slack app |
| `SLACK_SIGNING_SECRET` | Yes | Signing Secret from Slack app |
| `LOUIE_SITE_URL` | Yes | Base URL of Louie's website |
| `LOUIE_ADMIN_EMAIL` | Yes | Admin email for Payload CMS |
| `LOUIE_ADMIN_PASSWORD` | Yes | Admin password for Payload CMS |
| `ANTHROPIC_API_KEY` | Yes | For LLM-powered natural language parsing |
| `PORT` | No | Port to run on (Railway sets automatically) |
| `VERCEL_DEPLOY_HOOK_URL` | No | Webhook to trigger Vercel deployments |
| `SLACK_DEPLOY_CHANNEL` | No | Slack channel for deploy notifications |

## Monitoring

Railway provides:
- Real-time logs
- Deployment history
- Resource usage metrics
- Automatic restarts on failure

View logs: Project → Deployments → Click deployment → Logs tab

