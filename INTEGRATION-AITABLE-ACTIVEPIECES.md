# AITable.ai + Activepieces Integration Plan

## 🎯 Goal
Automate the **Draft → Edit → Publish** workflow without manual intervention.

---

## 📊 AITable.ai Setup

### Article Pipeline Table Structure

**Table: Articles**

| Field | Type | Description |
|-------|------|-------------|
| `title` | Single line text | Article title |
| `topic` | Single line text | Original topic/input |
| `status` | Single select | Draft / Editing / Published |
| `draft_content` | Long text | Generated draft |
| `edited_content` | Long text | After editing |
| `final_content` | Long text | Published version |
| `word_count` | Number | Word count |
| `generated_date` | Date | When draft was created |
| `published_date` | Date | When published |
| `publish_url` | URL | Link to published article |
| `platform` | Single select | Substack / WordPress / LinkedIn / etc |
| `notes` | Long text | Any notes/feedback |

**Views:**
- **Draft Queue** - Filter: `status = Draft`
- **Editing** - Filter: `status = Editing`
- **Published** - Filter: `status = Published`
- **This Week** - Filter: `generated_date` this week

---

## 🔄 Activepieces Workflows (No API Needed!)

**Note:** Activepieces works through webhooks and visual workflows - no API access required!

### Workflow 1: Auto-Track Generated Articles

**Trigger:** Webhook from VoiceCraft (when article generated)  
**Actions:**
1. Create record in AITable "Articles" table
2. Set status = "Draft"
3. Store draft_content, title, topic, word_count
4. Send notification (Slack/Email) with link to edit

**Setup:**
- VoiceCraft sends webhook → Activepieces receives it → Creates AITable record

### Workflow 2: Status Change Automation (Optional)

**Trigger:** AITable webhook (when status changes)  
**Actions:**
- **Draft → Editing:** Send reminder notification
- **Editing → Published:** 
  - Auto-publish to WordPress/Substack (via their APIs)
  - Update published_date in AITable
  - Store publish_url
  - Send confirmation

**Note:** This requires AITable webhook support or polling AITable for changes.

### Workflow 3: Weekly Article Generation (Optional)

**Trigger:** Schedule (Every Monday 9am)  
**Actions:**
1. HTTP request to VoiceCraft API endpoint
2. Receive generated article
3. Create AITable record as Draft
4. Notify you: "New draft ready for review"

**Note:** VoiceCraft API is already set up - just call it from Activepieces!

### Simplified Approach (Recommended)

Since Activepieces API requires sales contact, you can:
1. **Use AITable for tracking** (already integrated in VoiceCraft)
2. **Use VoiceCraft's built-in publishing** (WordPress/GitHub already work)
3. **Use Activepieces for simple automations** via webhooks (no API needed)

The main value is **AITable tracking** - Activepieces is nice-to-have for extra automation.

---

## 🔌 VoiceCraft API Integration

### Option 1: Webhook Integration (Recommended)

Modify VoiceCraft to send webhook after generation:

```python
# In core/workflow_automation.py
def _save_to_aitable(self, content: str, metadata: Dict):
    """Save generated content to AITable"""
    webhook_url = os.getenv('AITABLE_WEBHOOK_URL')
    if not webhook_url:
        return
    
    payload = {
        "title": metadata.get("title", "Untitled"),
        "topic": metadata.get("topic", ""),
        "status": "Draft",
        "draft_content": content,
        "word_count": len(content.split()),
        "generated_date": datetime.now().isoformat(),
        "platform": metadata.get("platform", "Substack")
    }
    
    requests.post(webhook_url, json=payload)
```

### Option 2: Activepieces Webhook Trigger

1. VoiceCraft generates article → saves locally
2. Activepieces watches file system or API endpoint
3. When new article detected → Create AITable record

---

## 🚀 Implementation Steps

### Step 1: Set Up AITable

1. Create "Articles" table with fields above
2. Create "Ideas" table for topic backlog
3. Set up views (Draft Queue, Editing, Published)
4. Get API token and base URL

### Step 2: Set Up Activepieces

1. Create workflow: "VoiceCraft → AITable"
2. Add webhook trigger (from VoiceCraft)
3. Add AITable action: Create record
4. Test with sample article

### Step 3: Modify VoiceCraft

1. Add AITable webhook URL to `.env.local`
2. Add `_save_to_aitable()` method
3. Call it after generation (before/after humanization)
4. Test integration

### Step 4: Set Up Publishing Workflows

1. Create workflow: "AITable Status Change → Publish"
2. Add WordPress/Substack actions
3. Test with draft article

---

## 📝 Example Workflow

**Your Process:**
1. You: "Generate article on 'AI expertise extraction'"
2. VoiceCraft: Generates draft → Saves to AITable (Status: Draft)
3. You: Review in AITable → Change status to "Editing"
4. You: Edit content in AITable → Update edited_content
5. You: Change status to "Published"
6. Activepieces: Auto-publishes to Substack → Updates publish_url

**Zero manual steps after initial generation!**

---

## 🔧 API Integration Details

### AITable.ai API

**Base URL:** `https://aitable.ai/api/v1/`

**Create Record:**
```python
POST /databases/{database_id}/tables/{table_id}/records
Headers: {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}
Body: {
    "fields": {
        "title": "Article Title",
        "status": "Draft",
        "draft_content": "...",
        "word_count": 1200
    }
}
```

### Activepieces Webhook

**Receive from VoiceCraft:**
```python
POST https://cloud.activepieces.com/api/v1/webhooks/{webhook_id}
Body: {
    "title": "...",
    "content": "...",
    "topic": "...",
    "word_count": 1200
}
```

---

## ✅ Benefits

1. **Zero Manual Tracking** - Everything auto-tracked in AITable ✅ (Works now!)
2. **Visual Pipeline** - See all articles at a glance ✅ (Works now!)
3. **Automated Publishing** - Use VoiceCraft's built-in WordPress/GitHub publishing
4. **Idea Management** - Backlog of topics in AITable ✅ (Works now!)
5. **Performance Tracking** - Add analytics later
6. **Simple Workflow** - Generate → Track in AITable → Edit → Publish via VoiceCraft

**Bottom Line:** AITable integration is the main value - it's already working! Activepieces is optional for extra automation.

---

## 🎯 Next Steps

1. **Set up AITable table** (5 minutes)
2. **Create Activepieces workflow** (10 minutes)
3. **Add webhook to VoiceCraft** (15 minutes)
4. **Test end-to-end** (5 minutes)

**Total: ~35 minutes to fully automate your workflow!**

---

## 📚 Resources

- [AITable API Docs](https://aitable.ai/api-docs)
- [Activepieces Docs](https://www.activepieces.com/docs)
- VoiceCraft API: `api/server.py`

