# VoiceCraft 🎨

**AI-powered content generation with style fusion technology**

Generate content in your voice, enhanced with stylistic elements from writers you admire.

---

## 🎯 Vision

VoiceCraft is an AI content generation platform that:
- Learns YOUR unique writing voice
- Blends in stylistic elements from writers you admire
- Generates content that sounds like you, but elevated
- Maintains brand consistency across all outputs
- Optimizes for AEO (AI Engine Optimization) automatically

**The Differentiator:** Not generic AI writing. Not expensive human writers. It's YOUR voice + the best elements of masters, at scale.

---

## 🚀 Core Features

### Phase 1: MVP (Current)
- [x] Project structure
- [ ] Style analyzer (extract writing patterns)
- [ ] Voice profile creator (learn your voice)
- [ ] Content generator with style fusion
- [ ] CLI tool for testing
- [ ] AEO optimization built-in

### Phase 2: Scale
- [ ] Web dashboard
- [ ] Multi-format output (articles, LinkedIn, Twitter, FAQs)
- [ ] Auto-publishing (GitHub, WordPress)
- [ ] Team collaboration
- [ ] Analytics & tracking

### Phase 3: Product
- [ ] Multi-tenant architecture
- [ ] Pre-loaded style library (famous writers)
- [ ] Custom style upload
- [ ] White-label option
- [ ] API access
- [ ] Billing integration

---

## 🧬 How Style Fusion Works

### 1. Base Voice Profile
Upload 3-5 pieces of YOUR content → System learns your:
- Vocabulary patterns
- Sentence structure preferences
- Tone and personality
- Content flow habits

### 2. Style Influences
Choose writers to influence your style:
- **Alex Hormozi** → Directness, urgency, bold claims
- **Seth Godin** → Brevity, insight, philosophical
- **Malcolm Gladwell** → Storytelling, narrative hooks
- **Custom** → Upload any writer's content

### 3. Blended Output
Generate content that:
- Maintains YOUR voice (60-70%)
- Incorporates stylistic elements (30-40%)
- Stays on-brand and authentic
- Optimized for AEO automatically

---

## 🏗️ Architecture

```
VoiceCraft/
├── core/                      # Core engine
│   ├── voice_processor.py     # Audio transcription
│   ├── style_analyzer.py      # Extract writing patterns
│   ├── voice_profiler.py      # Learn individual voices
│   ├── style_blender.py       # Blend multiple styles
│   ├── content_generator.py   # AI content generation
│   └── aeo_optimizer.py       # SEO/AEO optimization
├── styles/                    # Style library
│   ├── extractors/            # Analysis tools
│   ├── profiles/              # Pre-analyzed writers
│   └── custom/                # User-uploaded styles
├── api/                       # Backend API
│   └── main.py                # FastAPI server
├── frontend/                  # Web dashboard
│   └── (Next.js app)
├── cli/                       # Command-line tool
│   └── voicecraft.py          # CLI interface
└── data/                      # User data
    ├── voices/                # Voice profiles
    └── outputs/               # Generated content
```

---

## 🛠️ Tech Stack

**AI/ML:**
- OpenAI GPT-4 (content generation)
- Anthropic Claude (complex reasoning)
- Whisper API (voice transcription)
- spaCy (text analysis)

**Backend:**
- Python 3.11+
- FastAPI (API framework)
- PostgreSQL (data storage)
- Redis (caching/queue)

**Frontend:**
- Next.js 14
- Tailwind CSS
- Shadcn/ui components
- Recharts (analytics)

**Infrastructure:**
- Vercel (frontend hosting)
- Railway/Render (backend)
- Supabase (database + auth)

---

## 📦 Installation

```bash
# Clone the repo
cd VoiceCraft

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys (OpenAI, Anthropic, etc.)

# Run CLI tool
python cli/voicecraft.py --help
```

---

## 🎯 Quick Start

### Create Your Voice Profile
```bash
python cli/voicecraft.py profile create \
  --name "Louie Bernstein" \
  --samples "./samples/louie/*.md"
```

### Generate Content with Style Fusion
```bash
python cli/voicecraft.py generate \
  --profile "Louie Bernstein" \
  --input "Sales team optimization tips" \
  --influences "alex_hormozi:0.3,seth_godin:0.2" \
  --format article
```

### Analyze a Writer's Style
```bash
python cli/voicecraft.py style analyze \
  --name "Alex Hormozi" \
  --samples "./samples/hormozi/*.txt" \
  --output "./styles/profiles/alex_hormozi.json"
```

---

## 💰 Business Model (Future)

### Target Market
1. **Content creators** who want to write better, faster
2. **Marketing agencies** managing multiple client voices
3. **Consultants** who need consistent thought leadership
4. **B2B companies** scaling content operations

### Pricing Tiers
- **Personal:** $297/mo - Your voice + 2 influences
- **Professional:** $697/mo - Unlimited influences
- **Agency:** $1,497/mo - Multi-client + white-label

---

## 🎨 Unique Value Propositions

**vs ContentFly (Human Writers):**
- 10x faster (instant vs days)
- 5x cheaper ($297 vs $1500/mo)
- Perfectly consistent voice
- Unlimited revisions

**vs Jasper/Copy.ai (Generic AI):**
- Learns YOUR voice, not generic
- Style fusion from masters
- Maintains authenticity
- Built-in AEO optimization

**vs Hiring a Writer:**
- Scalable (1 writer vs unlimited)
- Learns continuously
- Never gets tired
- Perfect brand consistency

---

## 📊 Roadmap

### Month 1: MVP
- ✅ Core architecture
- [ ] Style analyzer working
- [ ] Basic content generation
- [ ] CLI tool functional
- [ ] Test with 2-3 voice profiles

### Month 2: Product
- [ ] Web dashboard
- [ ] Multi-format output
- [ ] Auto-publishing integrations
- [ ] 10 pre-analyzed style profiles
- [ ] Beta with 5-10 users

### Month 3: Scale
- [ ] Multi-tenant architecture
- [ ] Billing integration
- [ ] Marketing site
- [ ] Public launch
- [ ] First 50 paying customers

---

## 🤝 Contributing

This is currently a private project, but feedback is welcome!

---

## 📄 License

Proprietary - All rights reserved

---

## 🚀 Let's Build

**Status:** In active development  
**Current Phase:** MVP - Core Engine  
**Next Milestone:** Working style analyzer + content generator

---

Built with 🎨 by Max

