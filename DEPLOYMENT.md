# 🚀 Deployment Guide

## Current Setup

**Platform**: Cloudflare Pages  
**URL**: https://main.interdimensional-cable.pages.dev  
**Deploy Method**: Manual via Wrangler CLI  
**Source**: `public/` directory only

---

## Quick Deploy

```bash
# Deploy to Cloudflare Pages
npx wrangler pages deploy public --project-name=interdimensional-cable
```

That's it! The site will be live in ~30 seconds.

---

## What Gets Deployed

Only files in the `public/` directory:
- ✅ `index.html` - Main landing page
- ✅ `landing.html` - Alternative landing
- ✅ `embedding_flow.html` - Embedding flow viewer
- ✅ `debug.html` - Deployment debug page
- ✅ `channels_clustered_stream.json` - Channel configuration (80 channels, 1128 videos)
- ✅ `video_embeddings_with_urls.json` - Video embeddings (12MB, 1128 videos)

**What's excluded** (via `.wranglerignore`):
- ❌ Video files (*.mp4, *.mov, etc.)
- ❌ Video directories (channels/, generated_videos/, etc.)
- ❌ Cache files (*.pkl, video_embeddings_cache/)
- ❌ Development files (node_modules/, __pycache__/, etc.)

---

## Automatic Deployment (Recommended Setup)

To enable auto-deploy on every git push:

1. Go to https://dash.cloudflare.com/
2. Navigate to **Pages** → **interdimensional-cable**
3. Go to **Settings** → **Builds & deployments**
4. Click **"Connect to Git"**
5. Select **GitHub** and authorize
6. Choose repository: `voodoohop/interdimensionalcable`
7. Configure:
   - **Production branch**: `main`
   - **Build command**: (leave empty)
   - **Build output directory**: `public`
   - **Root directory**: (leave empty)

After setup, every `git push` will auto-deploy! 🎉

---

## File Structure

```
interdimensionalcable/
├── public/                          # ← DEPLOYED TO CLOUDFLARE
│   ├── index.html
│   ├── embedding_flow.html
│   ├── channels_clustered_stream.json
│   └── video_embeddings_with_urls.json
├── html_apps/                       # ← LOCAL DEVELOPMENT ONLY
│   └── tv_*.html                    # (not deployed)
├── wrangler.toml                    # Deployment config
└── .wranglerignore                  # Files to exclude
```

**Important**: 
- `public/` = Production (deployed)
- `html_apps/` = Development (local testing only)

---

## Common Issues & Solutions

### Issue: "ENOENT: no such file or directory" with video files
**Solution**: Videos are excluded via `.wranglerignore`. This is correct!

### Issue: Site shows old video count (894 instead of 1128)
**Solution**: 
1. Check `public/video_embeddings_with_urls.json` has correct count
2. Run `python3 scripts/utilities/export_embeddings_to_json.py`
3. Deploy: `npx wrangler pages deploy public --project-name=interdimensional-cable`

### Issue: Embedding flow can't find JSON
**Solution**: Paths in `public/embedding_flow.html` must use `/` not `../`

### Issue: Deployment takes forever
**Solution**: Make sure `.wranglerignore` is excluding video files

---

## Deployment Checklist

Before deploying:

- [ ] Videos uploaded to Cloudflare Stream? (via `upload_new_videos.py`)
- [ ] Channels JSON updated? (via `add_new_videos_to_channels.py` or `recluster_and_update_json.py`)
- [ ] Embeddings JSON updated? (via `export_embeddings_to_json.py`)
- [ ] Changes committed to git?
- [ ] Ready to deploy!

```bash
# Full workflow
python3 import_and_deploy_videos.py <source> --prefix <name> --recluster
python3 scripts/utilities/export_embeddings_to_json.py
git add public/
git commit -m "Update videos and embeddings"
git push
npx wrangler pages deploy public --project-name=interdimensional-cable
```

---

## Verify Deployment

```bash
# Check video count
curl -s https://main.interdimensional-cable.pages.dev/video_embeddings_with_urls.json | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(f'{data[\"total_videos\"]} videos')"

# Check channels
curl -s https://main.interdimensional-cable.pages.dev/channels_clustered_stream.json | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(f'{len(data[\"channels\"])} channels')"
```

Or visit: https://main.interdimensional-cable.pages.dev/debug.html

---

## URLs

- **Production**: https://main.interdimensional-cable.pages.dev
- **Embedding Flow**: https://main.interdimensional-cable.pages.dev/embedding_flow.html
- **Debug Page**: https://main.interdimensional-cable.pages.dev/debug.html
- **Cloudflare Dashboard**: https://dash.cloudflare.com/

---

## Notes

- Videos are hosted on **Cloudflare Stream** (separate from Pages)
- Only HTML/JSON/CSS/JS files are deployed to Pages
- Large files (12MB JSON) are fine, videos (GB+) are not
- Deployment takes ~30 seconds
- Cache may take 1-2 minutes to clear globally
