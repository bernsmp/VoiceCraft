# GitHub Setup for Railway Deployment

## Option 1: Create New GitHub Repo (Recommended)

### Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `VoiceCraft` (or your preferred name)
3. Description: "AI-powered content generation and website management"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have files)
6. Click **"Create repository"**

### Step 2: Push Local Code to GitHub

After creating the repo, GitHub will show you commands. Use these:

```bash
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/VoiceCraft.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/VoiceCraft.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Railway
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect GitHub account (if not already connected)
5. Search for **"VoiceCraft"** in the repository list
6. Select it and Railway will start deploying

---

## Option 2: Deploy Directly from Railway (No GitHub Needed)

Railway also supports deploying from:
- **GitHub** (most common)
- **GitLab**
- **Bitbucket**
- **Direct Git URL**

If you want to skip GitHub, you can:
1. Create a GitLab or Bitbucket repo instead
2. Or use Railway's CLI to deploy directly

---

## Option 3: Use Railway CLI (Alternative)

If you prefer not to use GitHub:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

## Troubleshooting: Can't Find Repo in Railway

**If Railway doesn't show your repo:**

1. **Check GitHub connection:**
   - Railway dashboard → Settings → GitHub
   - Make sure GitHub is connected
   - Reconnect if needed

2. **Check repository visibility:**
   - If repo is private, make sure Railway has access
   - Railway dashboard → Settings → GitHub → Check permissions

3. **Refresh Railway:**
   - Try refreshing the page
   - Or disconnect/reconnect GitHub

4. **Search for repo:**
   - In Railway's repo selector, use the search box
   - Type "VoiceCraft" or your repo name
   - Make sure you're searching in the right GitHub account/organization

5. **Check repo name:**
   - Make sure the repo name matches exactly
   - Case-sensitive: "VoiceCraft" vs "voicecraft"

---

## Quick Commands Summary

```bash
# Initialize git (if not done)
cd "/Users/maxb/Desktop/Vibe Projects/VoiceCraft"
git init
git add .
git commit -m "Add Slack bot integration and Railway deployment files"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/VoiceCraft.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Then in Railway:
1. New Project → Deploy from GitHub
2. Search for "VoiceCraft"
3. Select and deploy!

