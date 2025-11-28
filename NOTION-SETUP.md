# Notion Integration Setup

## 🎯 Why Notion?

You already work in Notion - why add another tool? Every article you generate will automatically appear in your Notion database.

---

## 🚀 5-Minute Setup

### Step 1: Create Notion Database (2 minutes)

1. **Create a new page** in Notion (or add to existing workspace)
2. **Type `/database`** and select "Table - Inline"
3. **Name it:** "Article Pipeline" or "VoiceCraft Articles"
4. **Add these properties:**

| Property Name | Type | Options |
|--------------|------|---------|
| `Title` | Title | (default) |
| `Topic` | Text | - |
| `Status` | Select | Draft, Editing, Published |
| `Word Count` | Number | - |
| `Platform` | Select | Substack, WordPress, LinkedIn |
| `Generated Date` | Date | - |
| `Published Date` | Date | - |
| `Publish URL` | URL | - |
| `Notes` | Text | - |

5. **Get your Database ID:**
   - Open the database
   - Click "..." menu → "Copy link"
   - The URL looks like: `https://www.notion.so/your-workspace/{DATABASE_ID}?v=...`
   - Copy the ID (32 characters, with hyphens)

### Step 2: Create Notion Integration (1 minute)

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Name it: "VoiceCraft"
4. Select your workspace
5. Click **"Submit"**
6. **Copy the "Internal Integration Token"** (starts with `secret_`)

### Step 3: Share Database with Integration (1 minute)

1. Go back to your Notion database
2. Click **"..."** menu → **"Connections"** → **"Add connections"**
3. Select your **"VoiceCraft"** integration
4. Click **"Confirm"**

### Step 4: Add to VoiceCraft (1 minute)

Add to `.env.local`:

```bash
NOTION_API_TOKEN=secret_your_token_here
NOTION_DATABASE_ID=your_database_id_here
```

### Step 5: Test

```bash
# Generate an article - it will auto-save to Notion
python3 cli/workflow.py create "Test article topic"
```

Check Notion - you should see a new page with:
- ✅ Title
- ✅ Topic
- ✅ Status: "Draft"
- ✅ Word count
- ✅ Full draft content in the page body

---

## ✅ That's It!

Now every article you generate will automatically:
- ✅ Appear in Notion as a new page
- ✅ Include all metadata (title, topic, word count, status)
- ✅ Have the full draft content in the page
- ✅ Be ready for your edit → publish workflow

**Your workflow:**
1. Generate article → Auto-saved to Notion (Draft) ✅
2. Edit in Notion → Change status to "Editing"
3. Mark as "Published" → Use VoiceCraft's built-in publishing to WordPress/Substack

---

## 🎨 Customize Your Database

### Add Views

Create filtered views:
- **Draft Queue** - Filter: `Status = Draft`
- **In Editing** - Filter: `Status = Editing`
- **Published** - Filter: `Status = Published`
- **This Week** - Filter: `Generated Date` this week

### Add Templates

Create a template for new articles with:
- Default status = "Draft"
- Pre-filled structure
- Your editing checklist

### Add Relations

Link articles to:
- Topics/Ideas database
- Publishing calendar
- Performance tracking

---

## 🔄 Your Complete Workflow

```
1. Generate article
   ↓
2. Auto-saved to Notion (Draft)
   ↓
3. Edit in Notion (change status to "Editing")
   ↓
4. Mark as "Published" in Notion
   ↓
5. Use VoiceCraft to publish to WordPress/Substack
   ↓
6. Update Notion with publish URL
```

**Everything in one place - Notion!**

---

## 🐛 Troubleshooting

### "Notion API token required"
- Make sure `NOTION_API_TOKEN` is set in `.env.local`
- Token should start with `secret_`

### "Notion database ID required"
- Make sure `NOTION_DATABASE_ID` is set
- Get it from the database URL (32 chars with hyphens)

### "Notion integration error: 401"
- Make sure you shared the database with your integration
- Go to database → "..." → "Connections" → Add your integration

### "Notion integration error: 403"
- Your integration doesn't have access
- Re-share the database with the integration

---

## 📚 Resources

- [Notion API Docs](https://developers.notion.com/)
- [Notion Integrations Guide](https://www.notion.so/help/add-and-manage-connections-with-the-api)

