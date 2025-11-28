# External System Guide - Input from Anywhere 🚀

## 🎯 The Real Value Proposition

**Input from anywhere, on the go → World-class content → Auto-published**

This is what makes VoiceCraft special - not just a tool, but a complete workflow automation system.

---

## 🏗️ What We Built

### 1. ✅ API Server (`api/server.py`)

**FastAPI-based REST API** for external integrations:
- Mobile apps
- Webhooks (Zapier, Make.com)
- Voice note services
- Email integrations
- Third-party tools

**Endpoints:**
- `POST /api/v1/quick` - Ultra-low friction content generation
- `POST /api/v1/content` - Full-featured content generation
- `POST /api/v1/voice-note` - Voice note processing
- `POST /api/v1/webhook` - Webhook integration
- `GET /api/v1/profiles` - List available profiles

---

### 2. ✅ WordPress Publishing

**Complete WordPress integration** via REST API:
- Auto-publish articles to WordPress
- Support for drafts, published, pending
- Categories and tags
- Featured images
- Application password authentication

**Configuration:**
```json
{
  "destination": "wordpress",
  "site_url": "yoursite.com",
  "app_password": "xxxx xxxx xxxx xxxx",
  "status": "draft"
}
```

---

### 3. ✅ GitHub Publishing (Enhanced)

**Already working**, now integrated with API:
- Auto-commit to GitHub repos
- Create/update files
- Full file path control

---

### 4. ✅ End-to-End Workflow

**Complete pipeline:**
```
Input (anywhere) → API → Generate → Humanize → Publish → Done ✅
```

---

## 🚀 Quick Start

### Start the API Server

```bash
cd /Users/maxb/Desktop/Vibe\ Projects/VoiceCraft
./api/start.sh
```

Or manually:
```bash
python3 -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

**Server:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs` (Swagger UI)

---

## 📱 Use Cases

### 1. Mobile Voice Notes

**Flow:**
1. Record voice note on phone
2. Transcribe (using Whisper, Otter.ai, etc.)
3. Send transcript to API
4. Get article back
5. Auto-publish to site

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/voice-note \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "So I was thinking about how AI is changing expertise...",
    "auto_publish": true,
    "publish_config": {
      "destination": "wordpress",
      "site_url": "yoursite.com",
      "status": "draft"
    }
  }'
```

---

### 2. Quick Ideas on the Go

**Flow:**
1. Text yourself an idea
2. Forward to API (via Zapier/webhook)
3. Get LinkedIn post
4. Auto-publish

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI reveals hidden expertise"
  }'
```

---

### 3. Client Content Pipeline

**Flow:**
1. Client sends idea (email, Slack, form)
2. Webhook triggers API
3. Generate content in client's voice
4. Auto-publish to their site
5. Notify client

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "content_request",
    "source": "client_portal",
    "data": {
      "input_text": "Sales team optimization strategies",
      "profile_name": "Louie Bernstein",
      "auto_publish": true,
      "publish_config": {
        "destination": "github",
        "repo": "louie/website",
        "file_path": "content/articles/sales-optimization.md"
      }
    }
  }'
```

---

## 🔗 Integration Examples

### Zapier Integration

1. **Trigger:** New email, form submission, etc.
2. **Action:** Webhook (POST to VoiceCraft API)
3. **Map fields:**
   - `event`: "content_request"
   - `data.input_text`: Your trigger field
   - `data.publish_config`: Publishing config

### Make.com (Integromat)

1. **Module:** HTTP Request
2. **Method:** POST
3. **URL:** `http://your-server:8000/api/v1/webhook`
4. **Body:** JSON with event and data

### Mobile App (React Native)

```javascript
async function createContent(topic) {
  const response = await fetch('http://your-server:8000/api/v1/quick', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      input_text: topic
    })
  });
  
  const result = await response.json();
  return result.content;
}
```

---

## 📤 Publishing Setup

### WordPress Setup

1. **Generate Application Password:**
   - Go to WordPress Admin → Users → Profile
   - Scroll to "Application Passwords"
   - Create new password
   - Copy the password (format: `xxxx xxxx xxxx xxxx`)

2. **Configure in API:**
   ```json
   {
     "destination": "wordpress",
     "site_url": "yoursite.com",
     "username": "your_username",
     "app_password": "xxxx xxxx xxxx xxxx",
     "status": "draft"
   }
   ```

3. **Or set environment variables:**
   ```bash
   WORDPRESS_USERNAME=your_username
   WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### GitHub Setup

1. **Create Personal Access Token:**
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate token with `repo` scope

2. **Set environment variable:**
   ```bash
   GITHUB_TOKEN=ghp_xxxxx
   ```

3. **Use in API:**
   ```json
   {
     "destination": "github",
     "repo": "username/repo",
     "file_path": "content/articles/my-article.md"
   }
   ```

---

## 🧪 Testing the System

### Test Quick Content

```bash
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "How AI is changing expertise"}'
```

### Test Voice Note

```bash
curl -X POST http://localhost:8000/api/v1/voice-note \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "So I was thinking about how AI is really changing the way we think about expertise. You know, it used to be that expertise was about knowing things, but now..."
  }'
```

### Test with Publishing

```bash
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI is changing expertise",
    "auto_publish": true,
    "publish_config": {
      "destination": "file",
      "file_path": "./test-output.md"
    }
  }'
```

---

## 🔐 Security (Production)

### API Key Authentication

1. **Set API key in `.env.local`:**
   ```bash
   VOICECRAFT_API_KEY=your-secret-key-here
   ```

2. **Uncomment validation in `api/server.py`:**
   ```python
   if x_api_key != os.getenv('VOICECRAFT_API_KEY'):
       raise HTTPException(status_code=401, detail="Invalid API key")
   ```

3. **Send key in requests:**
   ```bash
   curl -H "X-API-Key: your-secret-key-here" ...
   ```

### Rate Limiting (TODO)

Add rate limiting for production:
- Use `slowapi` or `fastapi-limiter`
- Limit requests per IP/user
- Protect against abuse

---

## 📊 Complete Workflow Example

### From Idea to Published Article

```bash
# 1. Send idea to API
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{"input_text": "How AI reveals hidden expertise"}'

# Response includes full article content

# 2. Or use full endpoint with auto-publish
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI reveals hidden expertise",
    "output_format": "article",
    "auto_humanize": true,
    "auto_publish": true,
    "publish_config": {
      "destination": "wordpress",
      "site_url": "yoursite.com",
      "status": "draft"
    }
  }'

# Result: Article generated, humanized, and published to WordPress as draft
```

---

## 🎯 Next Steps

### Immediate
- ✅ API server built
- ✅ WordPress publishing complete
- ✅ End-to-end workflow working

### Short-term
- [ ] Add API key authentication
- [ ] Add rate limiting
- [ ] Build mobile app example
- [ ] Create Zapier integration template
- [ ] Add webhook signature verification

### Long-term
- [ ] Build mobile app (React Native)
- [ ] Add scheduling (generate on schedule)
- [ ] Add batch processing endpoint
- [ ] Add content analytics
- [ ] Build admin dashboard

---

## 📚 Documentation

- **API Reference:** `http://localhost:8000/docs` (Swagger UI)
- **API README:** `api/README.md`
- **Workflow Guide:** `WORKFLOW-AUTOMATION.md`

---

**This is the real product** - Complete workflow automation from input to published content.

