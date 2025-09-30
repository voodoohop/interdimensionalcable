# 🎬 Interdimensional Cable - Project Structure

## 📁 Core Files

### 🖥️ TV Interface (For Public Access)
- **`tv_clustered.html`** - Main TV interface with 36 semantic clusters (⭐ PRIMARY)
- **`index.html`** - Landing page redirecting to TV interface
- **`channels_clustered.json`** - Channel configuration (local paths)
- **`channels_clustered_stream.json`** - Channel configuration with Cloudflare Stream URLs (generated)

### 📺 Legacy TV Apps (For Reference)
- **`tv_app.html`** - Simple 2-channel TV (original version)
- **`tv_channel_app.html`** - Alternative TV interface
- **`channels.json`** - Old channel config (flat structure)

---

## 🎥 Video Generation Scripts

### Active Generators
- **`enhanced_generator.py`** - Cinematic generator with 18 character prompts
- **`interdimensional_cable_generator.py`** - Original Veo 3 generator (text + init images)
- **`diverse_prompt_generator.py`** - 6-category prompt system (200+ variations)
- **`veo_init_image_prompts.py`** - Character archetypes library

### Download & Recovery
- **`immediate_video_saver.py`** - Real-time video downloader (fetchPredictOperation method)
- **`universal_video_saver.py`** - Batch recovery tool for all operations

---

## 📊 Clustering & Organization

### Active Tools
- **`advanced_video_clusterer.py`** - CLIP-based semantic clustering (36 clusters)
- **`semantic_video_analyzer.py`** - Video embeddings generator
- **`reorganize_by_clusters.py`** - Moves videos into cluster folders
- **`update_clustered_channels.py`** - Updates channels_clustered.json

### Helper Scripts
- **`update_channels.py`** - Updates simple channels.json
- **`setup_clustering.sh`** - One-line clustering setup
- **`check_clustering_progress.sh`** - Monitor clustering progress

---

## ☁️ Cloudflare Deployment

### Stream Upload (Currently Running)
- **`upload_to_stream.py`** - Batch upload 593 videos to Cloudflare Stream
- **`update_channels_with_stream.py`** - Generate Stream URL config
- **`stream_upload_progress.json`** - Upload progress tracker (auto-saved)
- **`stream_upload_results.json`** - Final results with video IDs (generated when complete)

### Cloudflare Config
- **`wrangler.toml`** - Cloudflare Pages/Workers configuration
- **`public/`** - Deployment directory for Pages

---

## 📚 Documentation

- **`README.md`** - Project overview
- **`STREAM_SETUP.md`** - Cloudflare Stream setup guide (⭐ SETUP GUIDE)
- **`CLUSTERING_README.md`** - Video clustering documentation
- **`prompting_guide.md`** - Veo 3 prompting tips
- **`PROJECT_STRUCTURE.md`** - This file

---

## 📦 Dependencies

- **`requirements.txt`** - Python packages (install with `pip install -r requirements.txt`)

**Key Dependencies:**
- `requests` - API calls
- `pillow` - Image processing
- `torch` - CLIP embeddings
- `transformers` - CLIP model
- `scikit-learn` - Clustering algorithms
- `google-auth` - Veo 3 authentication

---

## 🗂️ Data Directories (Gitignored)

### Video Collections
- **`channels_clustered/`** - 593 videos in 36 semantic clusters (4.8GB)
- **`channels/`** - Original flat channel structure
- **`generated_videos/`** - Veo 3 generated videos (~129 videos)
- **`init/`** - 6 init images for character generation

### Cache & Artifacts
- **`video_embeddings_cache/`** - Cached CLIP embeddings for clustering
- **`.wrangler/`** - Cloudflare local build cache
- **`public/`** - Cloudflare Pages deployment folder

---

## 🗄️ Backup Archive

All outdated/legacy files moved to **`backup/`**:

### `backup/old_operations/`
- Old operation JSONs from video generation sessions
- `cinematic_operations_*.json` (20+ files)
- `diverse_operations_*.json` (13+ files)
- `interdimensional_cable_operations.json`

### `backup/old_cluster_analysis/`
- Old clustering analysis and visualizations
- `cluster_analysis_size20.json`, `cluster_analysis_size50.json`
- `video_clusters_size20.png`, `video_clusters_size50.png`

### `backup/old_scripts/`
- Legacy/one-time-use scripts
- `check_init_image_videos.py`
- `comprehensive_status_check.py`
- `comprehensive_video_downloader.py`
- `crt_poster_variations.py`
- `download_existing_videos.py`
- `extract_screenshots.py`
- `filter_abstract_videos.py`
- `flatten_videos.py`
- `organize_ai_videos.py`
- `quick_download_check.py`
- `realtime_video_monitor.py`
- `reclassify_runway_videos.py`
- `video_downloader.py`
- `video_recovery_system.py`
- `veo3_js.js` (old JS version)
- `package.json` (node dependencies - not needed)

---

## 🚀 Quick Start Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Update channel config (if adding videos)
python3 update_clustered_channels.py
```

### Generate Videos
```bash
# Generate cinematic videos
python3 enhanced_generator.py cinematic 5

# Generate diverse content
python3 diverse_prompt_generator.py

# Download completed videos
python3 immediate_video_saver.py
```

### Deploy to Cloudflare
```bash
# 1. Upload videos (currently running)
python3 upload_to_stream.py

# 2. Generate Stream config (after upload completes)
python3 update_channels_with_stream.py

# 3. Deploy to Pages
mkdir -p public
cp tv_clustered.html public/
cp index.html public/
cp channels_clustered_stream.json public/channels_clustered.json
wrangler pages deploy public --project-name interdimensional-cable
```

### Local Testing
```bash
# Open TV interface locally
open tv_clustered.html

# View Stream analytics
open https://dash.cloudflare.com/stream
```

---

## 📊 Project Stats

- **Total Videos**: 593 videos (4.8GB)
- **Semantic Clusters**: 36 themed channels
- **Generated Videos**: ~129 from Veo 3 API
- **Init Images**: 6 Afrofuturistic characters
- **Cinematic Prompts**: 18 professional variations
- **Diverse Prompts**: 200+ across 6 categories

---

## 🎯 Current Status

✅ **Completed:**
- Video generation system fully operational
- CLIP-based semantic clustering (36 clusters)
- TV interface with retro CRT aesthetic
- Cloudflare Pages deployment setup

🔄 **In Progress:**
- Uploading 593 videos to Cloudflare Stream
- Process ID: 17306
- Progress saved to: `stream_upload_progress.json`

📋 **Next Steps:**
1. Wait for Stream upload to complete
2. Generate `channels_clustered_stream.json`
3. Deploy to Cloudflare Pages
4. Test live site and analytics

---

## 🎨 Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS (retro CRT aesthetic)
- **Video Generation**: Google Veo 3 API
- **Video Clustering**: OpenAI CLIP + scikit-learn
- **Video Hosting**: Cloudflare Stream
- **Deployment**: Cloudflare Pages
- **Backend Scripts**: Python 3.11+

---

## 💡 Key Features

- 🖥️ Retro CRT TV interface with green phosphor styling
- 🎬 36 semantically organized channels (no manual categorization!)
- 🎨 Professional cinematic video generation
- 📊 Cloudflare Stream analytics
- 🌍 Global CDN delivery
- 📱 Adaptive bitrate streaming
- ⌨️ Keyboard controls (↑↓ channels, SPACE play/pause, M mute)

---

## 📞 Contact & Credits

**Project**: Interdimensional Cable TV
**Generated**: 2025-09-29
**Videos**: AI-generated using Google Veo 3
**Clustering**: OpenAI CLIP embeddings
**Deployment**: Cloudflare Stream + Pages
