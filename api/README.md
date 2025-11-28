# VoiceCraft API Server

**External Input System** - Enable content creation from anywhere, on the go.

## 🎯 The Real Value

**Input from anywhere → World-class content → Auto-published**

This API enables:
- 📱 Mobile apps
- 🎤 Voice notes (transcripts)
- 🔗 Webhooks (Zapier, Make.com)
- 📧 Email integrations
- 🤖 Third-party services

---

## 🚀 Quick Start

### Start the Server

```bash
cd /Users/maxb/Desktop/Vibe\ Projects/VoiceCraft
python3 -m uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

Or use the included script:
```bash
python3 api/server.py
```

Server will be available at: `http://localhost:8000`

---

## 📡 API Endpoints

### 1. Quick Content (Recommended for Mobile)

**Endpoint:** `POST /api/v1/quick`

**Minimal input, maximum automation** - Perfect for mobile apps.

```bash
curl -X POST http://localhost:8000/api/v1/quick \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI is changing expertise"
  }'
```

**Response:**
```json
{
  "success": true,
  "content": "Full article content here...",
  "timestamp": "2025-01-23T10:30:00"
}
```

---

### 2. Full Content Generation

**Endpoint:** `POST /api/v1/content`

**Full control** - Specify input type, output format, publishing, etc.

```bash
curl -X POST http://localhost:8000/api/v1/content \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "How AI is changing expertise",
    "profile_name": "Max Bernstein",
    "output_format": "article",
    "target_length": 1500,
    "auto_humanize": true,
    "auto_publish": true,
    "publish_config": {
      "destination": "github",
      "repo": "username/repo",
      "file_path": "content/articles/ai-expertise.md"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "content": "Full article content...",
  "metadata": {
    "input_type": "topic",
    "output_format": "article",
    "output_path": "/path/to/output.md",
    "publish_result": {
      "success": true,
      "url": "https://github.com/username/repo/blob/main/content/articles/ai-expertise.md"
    }
  }
}
```

---

### 3. Voice Note Processing

**Endpoint:** `POST /api/v1/voice-note`

**Optimized for voice note transcripts** - Auto-cleans and formats.

```bash
curl -X POST http://localhost:8000/api/v1/voice-note \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "So I was thinking about how AI is really changing the way we think about expertise...",
    "output_format": "article",
    "auto_publish": true,
    "publish_config": {
      "destination": "wordpress",
      "site_url": "yoursite.com",
      "status": "draft"
    }
  }'
```

---

### 4. Webhook Endpoint

**Endpoint:** `POST /api/v1/webhook`

**For external integrations** (Zapier, Make.com, custom apps).

```bash
curl -X POST http://localhost:8000/api/v1/webhook \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "event": "content_request",
    "source": "mobile_app",
    "data": {
      "input_text": "How AI is changing expertise",
      "auto_publish": true,
      "publish_config": {
        "destination": "github",
        "repo": "username/repo"
      }
    }
  }'
```

---

## 🔐 Authentication

Currently, the API is open (for development). For production:

1. Set `VOICECRAFT_API_KEY` in `.env.local`
2. Uncomment API key validation in `api/server.py`
3. Send `X-API-Key` header with requests

---

## 📤 Publishing Configurations

### GitHub Publishing

```json
{
  "destination": "github",
  "repo": "username/repo",
  "file_path": "content/articles/my-article.md",
  "github_token": "optional-if-in-env"
}
```

**Environment Variable:** `GITHUB_TOKEN`

---

### WordPress Publishing

```json
{
  "destination": "wordpress",
  "site_url": "yoursite.com",
  "username": "wp_username",
  "app_password": "xxxx xxxx xxxx xxxx",
  "status": "draft",
  "categories": [1, 2],
  "tags": ["ai", "expertise"]
}
```

**Environment Variables:**
- `WORDPRESS_USERNAME`
- `WORDPRESS_PASSWORD` (or `WORDPRESS_APP_PASSWORD`)

**WordPress Setup:**
1. Go to Users → Profile
2. Generate Application Password
3. Use that password in `app_password` field

---

### File Publishing

```json
{
  "destination": "file",
  "file_path": "./published/my-article.md"
}
```

---

## 📱 Mobile App Integration Example

```javascript
// React Native / Mobile App Example
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

## 🔗 Zapier / Make.com Integration

### Zapier Webhook Trigger

1. Create new Zap
2. Trigger: Webhook by Zapier
3. Action: VoiceCraft API (`POST /api/v1/webhook`)
4. Map fields:
   - `event`: "content_request"
   - `data.input_text`: Your trigger field
   - `data.publish_config`: Your publishing config

---

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### List Profiles

```bash
curl http://localhost:8000/api/v1/profiles
```

---

## 🚀 Production Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using PM2

```bash
pm2 start "uvicorn api.server:app --host 0.0.0.0 --port 8000" --name voicecraft-api
```

### Using systemd

Create `/etc/systemd/system/voicecraft-api.service`:

```ini
[Unit]
Description=VoiceCraft API Server
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/VoiceCraft
ExecStart=/usr/bin/python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📝 Environment Variables

Create `.env.local` in project root:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Default Profile
VOICECRAFT_PROFILE=Max Bernstein

# Publishing
GITHUB_TOKEN=ghp_...
WORDPRESS_USERNAME=wp_user
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx

# API Security (for production)
VOICECRAFT_API_KEY=your-secret-api-key
```

---

## 🎯 Use Cases

### 1. Mobile Voice Notes
Record → Transcribe → Send to API → Get article → Auto-publish

### 2. Quick Ideas on the Go
Text message → API → LinkedIn post → Published

### 3. Batch Content Creation
CSV of topics → Process all → Auto-publish to site

### 4. Client Content Pipeline
Client sends idea → API → Generate → Review → Publish

---

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn api.server:app --port 8001
```

### API Key Issues

Check `.env.local` exists and has correct keys.

### Publishing Fails

- GitHub: Check token has repo write access
- WordPress: Verify app password is correct
- File: Check write permissions

---

## 📚 Next Steps

1. ✅ API server built
2. ✅ WordPress publishing complete
3. ⏳ Add authentication
4. ⏳ Add rate limiting
5. ⏳ Add webhook signatures
6. ⏳ Build mobile app examples

---

**This is the real product** - Input from anywhere, get world-class content automatically.

