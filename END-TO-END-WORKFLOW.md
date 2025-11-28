# End-to-End Workflow: Idea → Article → Posted on Site ✅

## 🎯 Complete Pipeline

**Input from anywhere → Generate → Humanize → Publish → Done**

This is the real value of VoiceCraft - complete workflow automation.

---

## 🚀 Quick Examples

### Example 1: Quick Idea → Published Article

```bash
# Start API server
./api/start.sh

# In another terminal, send idea
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI reveals hidden expertise",
    "output_format": "article",
    "auto_humanize": true,
    "auto_publish": true,
    "publish_config": {
      "destination": "file",
      "file_path": "./published/ai-expertise.md"
    }
  }'
```

**Result:** Article generated, humanized, and saved to file ✅

---

### Example 2: Voice Note → WordPress Draft

```bash
curl -X POST http://localhost:8000/api/v1/voice-note \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "So I was thinking about how AI is really changing the way we think about expertise. You know, it used to be that expertise was about knowing things, but now with AI, it's more about asking the right questions...",
    "auto_publish": true,
    "publish_config": {
      "destination": "wordpress",
      "site_url": "yoursite.com",
      "username": "wp_user",
      "app_password": "xxxx xxxx xxxx xxxx",
      "status": "draft"
    }
  }'
```

**Result:** Voice note processed, article generated, published to WordPress as draft ✅

---

### Example 3: Topic → GitHub Repository

```bash
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Sales team optimization strategies",
    "profile_name": "Louie Bernstein",
    "output_format": "article",
    "auto_publish": true,
    "publish_config": {
      "destination": "github",
      "repo": "username/repo",
      "file_path": "content/articles/sales-optimization.md"
    }
  }'
```

**Result:** Article generated in Louie's voice, published to GitHub ✅

---

## 📱 Mobile Workflow

### Using Mobile App / Voice Notes

1. **Record voice note** on phone
2. **Transcribe** (using Whisper, Otter.ai, etc.)
3. **Send to API:**
   ```javascript
   fetch('http://your-server:8000/api/v1/voice-note', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({
       transcript: voiceTranscript,
       auto_publish: true,
       publish_config: {
         destination: 'wordpress',
         site_url: 'yoursite.com',
         status: 'draft'
       }
     })
   })
   ```
4. **Get article back** - Already humanized and published ✅

---

## 🔗 Integration Workflows

### Zapier / Make.com

**Trigger:** New email, form submission, Slack message  
**Action:** VoiceCraft API  
**Result:** Content generated and published automatically

**Zapier Setup:**
1. Trigger: Email (Gmail)
2. Action: Webhook (POST to VoiceCraft API)
3. Map: Email body → `data.input_text`
4. Map: Publishing config → `data.publish_config`

---

## 🎯 Complete Use Cases

### Use Case 1: Content Creator

**Flow:**
- Record voice note while walking
- Send transcript to API
- Get LinkedIn post
- Auto-publish to LinkedIn (via integration)

### Use Case 2: Client Content Service

**Flow:**
- Client sends idea via form
- Webhook triggers API
- Generate in client's voice
- Auto-publish to client's WordPress site
- Email client with link

### Use Case 3: Batch Content Creation

**Flow:**
- CSV of topics
- Process each via API
- Generate articles
- Auto-publish all to site
- Done ✅

---

## 🔧 Configuration

### WordPress Publishing

**Setup:**
1. WordPress Admin → Users → Profile
2. Application Passwords → Create
3. Copy password (format: `xxxx xxxx xxxx xxxx`)

**Use:**
```json
{
  "destination": "wordpress",
  "site_url": "yoursite.com",
  "username": "wp_user",
  "app_password": "xxxx xxxx xxxx xxxx",
  "status": "draft"
}
```

### GitHub Publishing

**Setup:**
1. GitHub → Settings → Developer settings
2. Personal access tokens → Generate
3. Select `repo` scope

**Use:**
```json
{
  "destination": "github",
  "repo": "username/repo",
  "file_path": "content/articles/my-article.md"
}
```

**Environment Variable:**
```bash
GITHUB_TOKEN=ghp_xxxxx
```

---

## ✅ What's Working

- ✅ API server (`api/server.py`)
- ✅ Quick content endpoint (`/api/v1/quick`)
- ✅ Full content endpoint (`/api/v1/content`)
- ✅ Voice note endpoint (`/api/v1/voice-note`)
- ✅ Webhook endpoint (`/api/v1/webhook`)
- ✅ WordPress publishing
- ✅ GitHub publishing
- ✅ File publishing
- ✅ Auto-detection (input type, output format)
- ✅ Auto-humanization
- ✅ End-to-end workflow

---

## 🧪 Testing

### Test Quick Content

```bash
./api/test_api.sh
```

### Test Full Workflow

```bash
# Start server
./api/start.sh

# In another terminal
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Test article"}'
```

---

## 📚 Documentation

- **API Reference:** `http://localhost:8000/docs` (Swagger UI)
- **API Guide:** `api/README.md`
- **External System Guide:** `EXTERNAL-SYSTEM-GUIDE.md`
- **Workflow Automation:** `WORKFLOW-AUTOMATION.md`

---

**This is the real product** - Complete workflow automation from idea to published content.

