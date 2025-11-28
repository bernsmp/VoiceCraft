# AITable.ai Simple Setup (No Activepieces API Needed!)

## 🎯 What You Get

**Just AITable integration** - automatically track every article you generate in a visual database.

**No Activepieces API needed** - you can still use Activepieces for webhook-based workflows later if you want, but the main value is AITable tracking.

---

## 🚀 5-Minute Setup

### Step 1: Create AITable Table (2 minutes)

1. Go to [AITable.ai](https://aitable.ai/)
2. Create new database: "Article Pipeline"
3. Create table: "Articles"
4. Add these fields:

| Field Name | Type | Options |
|------------|------|---------|
| `title` | Single line text | - |
| `topic` | Single line text | - |
| `status` | Single select | Options: Draft, Editing, Published |
| `draft_content` | Long text | - |
| `edited_content` | Long text | - |
| `final_content` | Long text | - |
| `word_count` | Number | - |
| `generated_date` | Date | - |
| `published_date` | Date | - |
| `publish_url` | URL | - |
| `platform` | Single select | Options: Substack, WordPress, LinkedIn |
| `notes` | Long text | - |

5. **Get your IDs:**
   - Open your table
   - Database ID: From URL `https://aitable.ai/dst/{DATABASE_ID}/...`
   - Table ID: From URL `https://aitable.ai/dst/{DB_ID}/.../{TABLE_ID}`
   - API Token: Settings → API → Create token

### Step 2: Add to VoiceCraft (1 minute)

Add to `.env.local`:

```bash
AITABLE_API_TOKEN=your_token_here
AITABLE_BASE_URL=https://aitable.ai/api/v1
AITABLE_DATABASE_ID=your_database_id
AITABLE_TABLE_ID=your_table_id
```

### Step 3: Test (2 minutes)

```bash
# Generate an article - it will auto-save to AITable
python3 cli/workflow.py create "Test article topic"
```

Check AITable - you should see a new record with status "Draft"!

---

## ✅ That's It!

Now every article you generate will automatically:
- ✅ Appear in AITable as "Draft"
- ✅ Include title, topic, content, word count
- ✅ Be ready for your edit → publish workflow

**Your workflow:**
1. Generate article → Auto-saved to AITable (Draft)
2. Edit in AITable → Change status to "Editing"
3. Mark as "Published" → Use VoiceCraft's built-in publishing to WordPress/Substack

---

## 🔄 Optional: Activepieces Later

If you want to add Activepieces automation later (without API):
- Use webhook triggers (VoiceCraft → Activepieces webhook)
- Use AITable webhooks (if supported)
- Use scheduled workflows that call VoiceCraft API

But honestly, **AITable tracking alone is huge value** - you can see your entire pipeline at a glance!

