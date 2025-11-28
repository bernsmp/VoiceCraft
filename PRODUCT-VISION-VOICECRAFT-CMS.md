# VoiceCraft + CMS: AI-Managed Website Platform

## 🎯 Product Vision

**One-liner:** AI-powered website management where clients edit their site by talking to Slack, with content generated in their authentic voice.

**The Problem:**
- Small business owners/consultants don't have time to manage their website
- Hiring writers is expensive and voice consistency is hard
- Traditional CMS tools still require learning curves
- Content creation is a bottleneck for thought leaders

**The Solution:**
A complete website management system that combines:
1. **VoiceCraft** - AI content generation in the user's authentic voice
2. **Payload CMS** - Visual admin panel for manual control
3. **Slack Agent** - Natural language interface for quick updates
4. **Templated Sites** - Beautiful, fast Next.js sites ready to deploy

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT INTERFACES                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 Slack/Chat          💻 Admin Panel         🌐 Website    │
│  "Add article about     /admin                 Public site   │
│   cold calling"         Visual editing         louiebernstein│
│                         Payload CMS            .com          │
│                                                              │
└──────────────┬──────────────────┬──────────────┬────────────┘
               │                  │              │
               ▼                  ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    VOICECRAFT ENGINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🎨 Voice Profile       📝 Content Generator   🔄 Workflow   │
│  User's writing         AI writes in their     Automation    │
│  patterns analyzed      authentic voice        & deployment  │
│                                                              │
└──────────────┬──────────────────┬──────────────┬────────────┘
               │                  │              │
               ▼                  ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PAYLOAD CMS (API LAYER)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📄 Articles            🎬 Videos              ⚙️ Settings   │
│  Blog posts,            YouTube links,         Site config,  │
│  case studies           playlists              testimonials  │
│                                                              │
│  🔐 Auth                📊 Media               🔗 Webhooks   │
│  User management        Image uploads          Deploy hooks  │
│                                                              │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│                    NEXT.JS WEBSITE                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🏠 Homepage            📰 Articles            📺 Videos     │
│  Hero, services,        Blog/thought           Embedded      │
│  testimonials           leadership             playlists     │
│                                                              │
│  📧 Newsletter          📚 Course              📞 Contact    │
│  Signup CTA             Video course           Calendly      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 💬 User Flows

### Flow 1: Content Creation via Slack

```
User: "Write an article about why sales teams fail without documentation"

VoiceCraft Agent:
  1. Receives message in Slack
  2. Generates article outline
  3. Writes full article in user's voice (from voice profile)
  4. Creates article in Payload CMS via API
  5. Triggers Vercel deployment
  6. Responds: "✅ Article published: [link]"

User: "Actually, make the intro more punchy"

VoiceCraft Agent:
  1. Retrieves article from Payload
  2. Regenerates intro with style adjustment
  3. Updates article
  4. Redeploys
  5. Responds: "✅ Updated intro. Preview: [link]"
```

### Flow 2: Quick Updates via Slack

```
User: "Update the hero video to https://youtu.be/xyz123"

VoiceCraft Agent:
  1. Parses command
  2. Updates video field in Payload CMS
  3. Triggers deployment
  4. Responds: "✅ Hero video updated and deployed"

User: "Add a testimonial from John at Acme Corp - 'Louie helped us 2x our sales'"

VoiceCraft Agent:
  1. Creates testimonial in Payload
  2. Deploys
  3. Responds: "✅ Testimonial added to homepage"
```

### Flow 3: Manual Editing via Admin Panel

```
User visits: louiebernstein.com/admin
  → Logs in
  → Sees dashboard with:
     - Recent articles
     - Site stats
     - Quick actions
  → Clicks "Articles" → Edits existing article
  → Clicks "Save" → Auto-deploys
```

---

## 📦 Content Types (Payload Schema)

### Articles
```typescript
{
  title: string,
  slug: string,
  content: richText,
  excerpt: string,
  author: relationship → Users,
  publishDate: date,
  featured: boolean,
  seoTitle: string,
  seoDescription: string,
  ogImage: media,
  tags: array<string>,
  status: 'draft' | 'published',
  // VoiceCraft metadata
  generatedBy: 'human' | 'ai',
  voiceProfile: string,
  styleInfluences: array<string>,
}
```

### Videos
```typescript
{
  title: string,
  youtubeId: string,
  description: text,
  category: 'hero' | 'course' | 'shorts' | 'playlist',
  displayOrder: number,
  featured: boolean,
}
```

### Testimonials
```typescript
{
  quote: text,
  author: string,
  company: string,
  role: string,
  featured: boolean,
  displayOrder: number,
}
```

### Site Settings
```typescript
{
  heroTagline: string,
  heroSubtagline: string,
  ctaPrimary: { text: string, url: string },
  ctaSecondary: { text: string, url: string },
  socialLinks: {
    linkedin: string,
    youtube: string,
    twitter: string,
  },
  contactEmail: string,
  calendlyUrl: string,
}
```

---

## 🔌 VoiceCraft Integration Points

### Slack Commands

**Website Editing (IMPLEMENTED):**
```
/site show                       → View current site settings
/site help                       → Show all available commands
/site headline "New Text"        → Update hero headline
/site tagline "New Text"         → Update hero tagline
/site video ABC123               → Update YouTube video ID
/site email "new@email.com"      → Update contact email
/site phone "(555) 123-4567"     → Update phone number
```

**Natural Language Editing (IMPLEMENTED):**
```
"Change the headline to 'Sales Expert'"
"Update the tagline to 'More Sales'"
"Set the phone number to (404) 555-1234"
"What's the current hero description?"
```

**Content Generation (Coming Soon):**
```
/vc article "topic"              → Generate and publish article
/vc article draft "topic"        → Generate draft (don't publish)
/vc edit article [slug] "..."    → Edit existing article
/vc testimonial "quote" - Name   → Add testimonial
/vc deploy                       → Force deployment
/vc status                       → Show site status
```

### Payload Webhooks → VoiceCraft

```typescript
// When content changes in Payload, notify VoiceCraft
hooks: {
  afterChange: async ({ doc, operation }) => {
    await notifyVoiceCraft({
      event: operation, // 'create' | 'update' | 'delete'
      collection: 'articles',
      doc: doc,
    });
  }
}
```

### VoiceCraft → Payload API

```typescript
// VoiceCraft creates content via Payload REST API
await fetch('https://louiebernstein.com/api/articles', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${PAYLOAD_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: generatedTitle,
    content: generatedContent,
    generatedBy: 'ai',
    voiceProfile: 'louie_bernstein',
    status: 'published',
  }),
});
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────┐
│              Vercel                      │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Next.js + Payload CMS          │ │
│  │                                    │ │
│  │  /          → Public website       │ │
│  │  /admin     → Payload admin        │ │
│  │  /api/*     → Payload REST API     │ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│                    │                     │
│                    ▼                     │
│  ┌────────────────────────────────────┐ │
│  │     MongoDB Atlas (Free Tier)      │ │
│  │     or Vercel Postgres             │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              │
              │ Slack Events API
              ▼
┌─────────────────────────────────────────┐
│         VoiceCraft Agent                 │
│         (Railway / Render)               │
│                                          │
│  - Slack bot server                      │
│  - Voice profiles                        │
│  - Content generation                    │
│  - Payload API client                    │
└─────────────────────────────────────────┘
```

---

## 💰 Productization Path

### Phase 1: Louie's Site (Current)
- [ ] Add Payload CMS to existing site
- [ ] Migrate content to Payload
- [ ] Connect VoiceCraft Slack bot
- [ ] Test full workflow
- **Goal:** Working proof-of-concept

### Phase 2: Template System
- [ ] Extract site as reusable template
- [ ] Parameterize branding (colors, fonts, logos)
- [ ] Create setup scripts
- [ ] Document deployment process
- **Goal:** Deploy new client site in < 1 hour

### Phase 3: Multi-Tenant Platform
- [ ] Central VoiceCraft instance
- [ ] Per-client voice profiles
- [ ] Per-client Payload instances
- [ ] Unified billing
- **Goal:** SaaS-ready platform

### Phase 4: Self-Service
- [ ] Marketing site
- [ ] Onboarding flow
- [ ] Stripe integration
- [ ] Auto-provisioning
- **Goal:** Customers can sign up and deploy

---

## 💵 Pricing Model (Future)

| Tier | Price | What's Included |
|------|-------|-----------------|
| **Starter** | $297/mo | Site + CMS + 5 AI articles/mo |
| **Growth** | $497/mo | + Unlimited AI content + Slack bot |
| **Agency** | $997/mo | + Multiple sites + White-label |

**Revenue per client:** $3,564 - $11,964/year

---

## 🎯 Unique Value Proposition

**vs. Webflow/Squarespace:**
- AI writes content in YOUR voice
- Manage via Slack, not complex UI
- Built for thought leaders, not generic sites

**vs. WordPress + Writers:**
- 10x faster content creation
- Perfect voice consistency
- Fraction of the cost

**vs. Other AI Tools:**
- Complete website, not just content
- Visual CMS for control
- Voice profiles, not generic AI

---

## 📋 Implementation Checklist

### Payload CMS Setup (Louie's Site)
- [x] Install Payload in Next.js project ✅
- [x] Configure MongoDB Atlas (free tier) ✅
- [x] Define content schemas (Articles, Videos, Testimonials, Settings) ✅
- [x] Customize admin branding (Louie's colors/logo) ✅
- [x] Set up API authentication ✅
- [x] Expanded SiteSettings for full website copy editing ✅
- [ ] Migrate existing content to Payload
- [x] Update site to pull from Payload (Hero, ValueProp, Contact) ✅
- [ ] Deploy CMS integration to Vercel

### VoiceCraft Integration
- [x] Create Payload API client in VoiceCraft (`integrations/cms_integration.py`) ✅
- [x] Add website management commands to Slack bot ✅
- [x] Natural language parsing for edits ✅
- [ ] Set up deploy webhook
- [ ] Test article creation flow
- [ ] Test video update flow
- [ ] Test testimonial flow

### Testing & Polish
- [ ] Full user flow testing
- [ ] Error handling
- [ ] Slack response formatting
- [x] Admin panel branding ✅
- [ ] Performance optimization

---

## 🗂️ File Structure (After Implementation)

```
louiebernstein-website/
├── app/
│   ├── (frontend)/          # Public pages
│   │   ├── page.tsx
│   │   ├── articles/
│   │   └── ...
│   └── (payload)/           # Payload admin
│       └── admin/
├── payload/
│   ├── payload.config.ts    # Main config
│   ├── collections/
│   │   ├── Articles.ts
│   │   ├── Videos.ts
│   │   ├── Testimonials.ts
│   │   └── Settings.ts
│   ├── components/          # Custom admin components
│   └── hooks/               # Webhooks & automation
├── lib/
│   └── payload.ts           # Payload client
└── ...

VoiceCraft/
├── integrations/
│   ├── slack_bot.py           # Slack interface (UPDATED with /site commands)
│   ├── slack_bot_server.py    # Flask server for Slack events
│   ├── cms_integration.py     # Payload API client + natural language parser
│   └── SLACK-CMS-SETUP.md     # Setup guide
├── core/
│   └── ...                    # Existing VoiceCraft core
└── data/
    └── voices/
        └── louie_bernstein.json
```

---

## 🔜 Next Steps

1. **Add Payload CMS to Louie's site** (~3-4 hours)
2. **Define content schemas** (~1 hour)
3. **Migrate content** (~2 hours)
4. **Build VoiceCraft Payload client** (~2 hours)
5. **Add Slack commands** (~2 hours)
6. **Test full flow** (~2 hours)

**Total estimated time:** ~12-14 hours

---

*Document created: November 25, 2025*
*First client: Louie Bernstein (louiebernstein.com)*
*Vision: AI-Managed Website Platform*

