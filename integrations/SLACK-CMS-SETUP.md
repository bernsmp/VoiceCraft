# VoiceCraft + Website CMS Integration

Edit your website through Slack! This integration connects VoiceCraft's Slack bot to Payload CMS (or AITable) for natural language website editing.

## Phase 1 Complete ✅
- **Seed script**: Populates Payload CMS with defaults (idempotent, JWT auth)
- **Merge logic**: Site uses CMS data when present; falls back to defaults only when undefined/null
- **AITable adapter**: Scaffolded for Phase 2 (feature-flag enabled)

## Phase 2 Complete ✅
- **LLM parsing**: Claude Opus 4.5 parses ambiguous commands; pattern matching for simple edits
- **Slack posting**: Bot posts responses (no prints); threads replies; handles DMs/channels
- **Confirmation flow**: Preview changes with Confirm/Cancel buttons; apply only on confirm
- **Auth hardening**: Token refresh/cache; exponential backoff retries for transient failures
- **Deploy webhooks**: Trigger Vercel deploy after CMS updates; notify Slack on deploy status

## Quick Setup

### 1. Environment Variables

Add these to your environment or `.env` file:

```bash
# Louie's Website CMS (Payload)
LOUIE_SITE_URL=https://louiebernstein.com
LOUIE_ADMIN_EMAIL=louis30092@gmail.com
LOUIE_ADMIN_PASSWORD=DoneGood#
# Optional: API key auth (recommended)
# PAYLOAD_API_KEY=

# AITable (optional, for Phase 2+)
# USE_AITABLE_CMS=true
# AITABLE_API_KEY=
# AITABLE_BASE_ID=
# AITABLE_DATASHEET_ID=

# Slack Bot
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# LLM parsing (for ambiguous commands)
ANTHROPIC_API_KEY=

# Deploy webhooks (optional)
VERCEL_DEPLOY_HOOK_URL=
SLACK_DEPLOY_CHANNEL=#website-updates
```

### 2. Install Dependencies

```bash
pip install flask requests python-dotenv slack-sdk anthropic
```

### 3. Start the Bot

```bash
python integrations/slack_bot_server.py
```

Or use ngrok for local development:

```bash
ngrok http 3001
```

## Slack Commands

### Website Editing

```
/site show           - View current settings
/site help           - Show all commands
/site headline "New Headline"
/site tagline "New Tagline"  
/site video fCVKpcpD8tA
/site email "new@email.com"
```

### Natural Language (Just Chat!)

- "Change the headline to 'Sales Leadership Expert'"
- "Update the tagline to 'Less Spend. More Sales.'"
- "Set the phone number to (404) 808-5326"
- "What's the current hero description?"

### Content Generation

```
/content "Why Cold Calling Still Works in 2025"
/content-voice [paste your voice transcript]
/content-blend "Sales Tips" Hormozi:30
```

## Editable Fields

| Field | Description | Example |
|-------|-------------|---------|
| headline | Main hero heading | "Fractional Sales Leader" |
| tagline | Hero subheadline | "Less Spend. More Sales." |
| description | Hero body text | "I've scaled from zero..." |
| video | YouTube video ID | "fCVKpcpD8tA" |
| credential | Badge primary text | "LinkedIn Top Voice" |
| email | Contact email | "Louie@LouieBernstein.com" |
| phone | Contact phone | "(404)808-5326" |
| linkedin | LinkedIn URL | Full URL |
| youtube | YouTube URL | Full URL |
| calendly | Calendly URL | Full URL |
| cta | Call-to-action text | "Schedule a Discussion" |
| site title | SEO title | For search results |
| site description | SEO description | For search results |
| keywords | SEO keywords | Comma-separated |

## Phase 2 Features

### LLM-Powered Parsing
For ambiguous commands, the bot uses Claude Opus 4.5:
- **Pattern matching (fast)**: "Change headline to X" → direct field match
- **LLM fallback**: "Make the main title say X" → Claude parses intent
- **Better errors**: Suggests similar fields when match fails

### Confirmation Flow
Changes are previewed before applying:
1. Bot shows preview with current/new values
2. User clicks ✅ Confirm or ❌ Cancel buttons
3. Only applies change after confirmation

### Auth & Retries
- Token caching with auto-refresh (6-day expiry)
- Exponential backoff for 5xx/429 errors (3 retries max)
- Timeout protection (10s per request)

### Deploy Webhooks
After CMS updates:
- Triggers Vercel deploy via webhook
- Notifies Slack: 🚀 started → ✅ success
- Optional: Payload `afterChange` hook for auto-deploys

## Architecture

```
┌─────────────────────────────────────────┐
│                 Slack                    │
│  User: "Change headline to 'Expert'"   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          VoiceCraft Slack Bot           │
│  - Pattern match or LLM parse           │
│  - Show preview + Confirm/Cancel        │
│  - On confirm: update CMS               │
└─────────────────┬───────────────────────┘
                  │
         ┌────────┼────────┐
         │                │
         ▼                ▼
┌────────────┐   ┌────────────────┐
│ Payload CMS │   │ Claude Opus 4.5 │
│ (JWT auth)  │   │ (LLM parsing)   │
└─────┬───────┘   └────────────────┘
      │ (afterChange hook)
      ▼
┌─────────────────┐
│ Vercel Deploy  │
│ (via webhook)  │
└─────┬────────────┘
      ▼
┌─────────────────┐
│ Live Website   │
│ (ISR ~60s)     │
└─────────────────┘
```

## Testing Locally

```python
from integrations.cms_integration import WebsiteEditor

editor = WebsiteEditor("louie")
result = editor.process_command("Change the headline to 'Test'")
print(result)
```

## Adding More Websites

Edit `integrations/cms_integration.py`:

```python
WEBSITES = {
    "louie": CMSConfig(
        name="Louie Bernstein",
        base_url="https://louiebernstein.com",
        admin_email="...",
        admin_password="...",
    ),
    "new_client": CMSConfig(
        name="New Client",
        base_url="https://newclient.com",
        admin_email="...",
        admin_password="...",
    ),
}
```

Then update the Slack bot to handle multiple sites or use a default.

