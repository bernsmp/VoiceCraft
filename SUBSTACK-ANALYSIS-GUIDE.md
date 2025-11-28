# Substack Article Performance Analysis Guide

## 🎯 What This Does

Analyzes your Substack articles to:
1. **Identify top performers** - Most popular/engaging articles
2. **Rank by engagement** - Views, likes, comments, shares
3. **Analyze why they worked** - Hook patterns, structure, content elements
4. **Generate insights** - What to replicate in future articles

---

## 🚀 Quick Start

### Step 1: Extract Articles (if not already done)

```bash
python3 scripts/extract_substack_articles.py https://irreplaceablepositioning.substack.com 50
```

This saves articles to `./data/samples/`

### Step 2: (Optional) Add Engagement Data

Create `./data/substack_engagement.json`:

```json
{
  "https://irreplaceablepositioning.substack.com/p/article-1": {
    "views": 1500,
    "likes": 75,
    "comments": 12,
    "shares": 8
  },
  "https://irreplaceablepositioning.substack.com/p/article-2": {
    "views": 2000,
    "likes": 100,
    "comments": 20,
    "shares": 15
  }
}
```

**How to get engagement data:**
1. Go to Substack dashboard → Analytics
2. Export or manually copy metrics
3. Create JSON file with URL → metrics mapping

### Step 3: Run Analysis

```bash
python3 scripts/analyze_substack_performance.py
```

**Output:**
- `./data/substack_analysis_report.md` - Full analysis report
- Console output with top performers

---

## 📊 What Gets Analyzed

### Content Analysis (Automatic)

Even without engagement data, the script analyzes:

1. **Hook Quality**
   - First paragraph length
   - Direct address ("you", "your")
   - Question patterns

2. **Structure**
   - Paragraph count
   - Heading usage
   - List usage
   - Average paragraph length

3. **Content Signals**
   - Examples/stories
   - Questions (engagement)
   - Value keywords (insight, framework, etc.)

### Deep Analysis (Requires API Key)

With Anthropic API key, analyzes:
- Why top articles worked
- Hook patterns
- Structure patterns
- Content elements
- Engagement triggers
- Voice/tone patterns
- Actionable takeaways

---

## 📈 Understanding the Report

### Top 10 Ranking

Shows:
- Engagement score (higher = better)
- Views, likes, comments, shares
- Word count
- Hook preview
- Structure breakdown

### Why Top Articles Worked

AI analysis of:
- What made hooks effective
- Structure patterns that work
- Content elements that drive engagement
- Voice/tone that resonates

### Patterns to Replicate

Actionable insights on:
- Hook patterns to use
- Structure approaches
- Content elements to include
- Engagement triggers to leverage

---

## 🔧 Advanced Usage

### Custom Engagement Data

**CSV Format** (`data/substack_engagement.csv`):
```csv
url,views,likes,comments,shares
https://irreplaceablepositioning.substack.com/p/article-1,1500,75,12,8
https://irreplaceablepositioning.substack.com/p/article-2,2000,100,20,15
```

**JSON Format** (`data/substack_engagement.json`):
```json
{
  "article_url": {
    "views": 1000,
    "likes": 50,
    "comments": 10,
    "shares": 5
  }
}
```

### Analyze Specific Articles

Modify the script to filter articles:
```python
# In analyze_substack_performance.py
articles = analyzer.load_articles()
# Filter by date, title, etc.
filtered = [a for a in articles if "keyword" in a['title']]
```

---

## 💡 Use Cases

### 1. Find Your Best Content

See which articles resonated most with readers.

### 2. Identify Patterns

Understand what makes your top articles work.

### 3. Replicate Success

Use insights to create more high-performing content.

### 4. Content Strategy

Identify topics/formats that drive engagement.

---

## 🎯 Next Steps

1. **Run analysis** on your articles
2. **Review report** to see top performers
3. **Analyze patterns** in successful articles
4. **Apply insights** to future content
5. **Track results** and iterate

---

## 📝 Notes

- **No engagement data?** Script uses content analysis to estimate performance
- **Want real metrics?** Export from Substack dashboard and create JSON file
- **Need deeper analysis?** Set `ANTHROPIC_API_KEY` for AI-powered insights

---

**Ready to analyze your Substack performance!**

