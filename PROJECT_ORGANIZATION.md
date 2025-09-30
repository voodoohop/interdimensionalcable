# 📁 Project Organization Guide

## Directory Structure

### 🎬 `/scripts/` - All Python Scripts Organized by Function

#### `/scripts/veo_generation/` - Veo 3 Video Generation
- **`interdimensional_cable_generator.py`** - Main Veo 3 text-to-video generator
- **`enhanced_generator.py`** - Cinematic character-based generator (18 prompts, 6 characters)
- **`diverse_prompt_generator.py`** - Multi-category prompt system (abstract, nature, retro, etc.)
- **`veo_init_image_prompts.py`** - Prompt library for image-to-video generation
- **`immediate_video_saver.py`** - Real-time video download monitoring
- **`universal_video_saver.py`** - Batch video recovery from operation files
- **`download_runway_videos.py`** - Runway ML video downloader

**Usage:**
```bash
# Generate cinematic videos
python3 scripts/veo_generation/enhanced_generator.py cinematic 5

# Generate diverse content
python3 scripts/veo_generation/diverse_prompt_generator.py generate 10

# Download completed videos
python3 scripts/veo_generation/universal_video_saver.py
```

#### `/scripts/clustering/` - Video Semantic Clustering
- **`advanced_video_clusterer.py`** - Main clustering engine with CLIP embeddings
- **`semantic_video_analyzer.py`** - Video semantic analysis and embedding generation
- **`apply_clustering_results.py`** - Apply clustering results to organize videos
- **`reorganize_by_clusters.py`** - Reorganize videos into cluster folders
- **`prepare_combined_clustering.py`** - Prepare videos for combined clustering
- **`setup_clustering.sh`** - Setup script for clustering environment
- **`check_clustering_progress.sh`** - Monitor clustering progress

**Usage:**
```bash
# Run clustering
python3 scripts/clustering/advanced_video_clusterer.py --input videos_combined_for_clustering/ --output channels_reclustered_all/

# Check progress
bash scripts/clustering/check_clustering_progress.sh
```

#### `/scripts/stream_upload/` - Cloudflare Stream Upload
- **`upload_to_stream.py`** - Main upload script for Cloudflare Stream
- **`update_channels_with_stream.py`** - Update channel configs with Stream URLs
- **`run_upload.sh`** - Bash wrapper for upload process

**Usage:**
```bash
# Upload videos to Cloudflare Stream
bash scripts/stream_upload/run_upload.sh

# Or directly
python3 scripts/stream_upload/upload_to_stream.py
```

#### `/scripts/utilities/` - Helper Scripts
- **`cleanup_duplicates.py`** - Remove duplicate videos across channels
- **`update_channels.py`** - Update channels.json from folder structure
- **`update_clustered_channels.py`** - Update clustered channels config

**Usage:**
```bash
# Clean duplicates
python3 scripts/utilities/cleanup_duplicates.py

# Update channel configs
python3 scripts/utilities/update_channels.py
```

### 🖥️ `/html_apps/` - Web Applications
- **`tv_clustered_stream.html`** - **MAIN APP** - Full TV with Cloudflare Stream (PRODUCTION)
- **`tv_clustered.html`** - TV app with local clustered videos
- **`tv_app.html`** - Original simple TV app
- **`tv_channel_app.html`** - Alternative TV channel interface

**Access:** Open `index.html` in root (redirects to main app)

### 📊 `/docs/` - Documentation & Reports
- Clustering reports, session summaries, project structure docs
- Upload progress tracking files
- Generated documentation

### 📹 `/channels_reclustered_all/` - Organized Video Library
- 67 semantic clusters (01_Cluster_0 through 67_Cluster_66)
- Videos organized by AI-detected themes
- **Total:** 1,000+ videos across all clusters

### 🎨 `/init/` - Init Images for Image-to-Video
- 6 Afrofuturistic character images (init_01.jpeg through init_06.jpeg)
- Used by enhanced_generator.py for character-consistent videos

### 🗄️ `/archived/` - Outdated/One-Time Scripts
- **`create_test_config.py`** - Test config creator (no longer needed)
- **`fix_progress_file.py`** - Progress file fixer (one-time use)
- **`test_stream_urls.py`** - Stream URL tester (debugging tool)
- **`fix_stream_urls.sh`** - URL fix script (one-time use)
- Old upload logs and visualization PNGs

### 📝 Root Configuration Files
- **`.env`** - Environment variables (Cloudflare API token)
- **`channels.json`** - Original channel configuration
- **`channels_clustered.json`** - Clustered channel configuration (local)
- **`channels_clustered_stream.json`** - Clustered channels with Stream URLs (PRODUCTION)
- **`stream_upload_results.json`** - Upload results tracking
- **`requirements.txt`** - Python dependencies
- **`wrangler.toml`** - Cloudflare Workers config
- **`index.html`** - Entry point (redirects to main app)

## 🚀 Quick Start Commands

### Generate New Videos
```bash
# Cinematic character videos (Veo 3)
python3 scripts/veo_generation/enhanced_generator.py cinematic 5

# Diverse abstract/nature videos
python3 scripts/veo_generation/diverse_prompt_generator.py generate 10
```

### Organize & Cluster Videos
```bash
# Run semantic clustering
python3 scripts/clustering/advanced_video_clusterer.py

# Reorganize into clusters
python3 scripts/clustering/reorganize_by_clusters.py
```

### Upload to Cloudflare Stream
```bash
# Upload all videos
bash scripts/stream_upload/run_upload.sh

# Update channel configs with Stream URLs
python3 scripts/stream_upload/update_channels_with_stream.py
```

### View TV App
```bash
# Open in browser
open index.html
# Or directly:
open html_apps/tv_clustered_stream.html
```

## 📊 Current Stats
- **Videos Generated:** 1,000+ videos
- **Clusters:** 67 semantic clusters
- **Total Size:** ~5GB+ of video content
- **Uploaded to Stream:** 1,000+ videos on Cloudflare Stream
- **Characters:** 6 Afrofuturistic archetypes
- **Prompt Categories:** 7 (cinematic, abstract, nature, retro, architectural, weather, microscopic)

## 🔧 Maintenance

### Clean Up Duplicates
```bash
python3 scripts/utilities/cleanup_duplicates.py
```

### Update Channel Configs
```bash
python3 scripts/utilities/update_channels.py
```

### Check Clustering Progress
```bash
bash scripts/clustering/check_clustering_progress.sh
```

## 📚 Key Documentation
- **`README.md`** - Project overview
- **`STATUS.md`** - Current project status
- **`NEXT_SESSION.md`** - Next session tasks
- **`DUPLICATE_CLEANUP_GUIDE.md`** - Duplicate cleanup guide
- **`RUNWAY_UI_DOWNLOAD.md`** - Runway video download guide
- **`docs/CLUSTERING_README.md`** - Clustering system documentation
- **`docs/PROJECT_STRUCTURE.md`** - Detailed project structure

## 🎯 Production Workflow

1. **Generate Videos** → `scripts/veo_generation/`
2. **Cluster Videos** → `scripts/clustering/`
3. **Upload to Stream** → `scripts/stream_upload/`
4. **View in TV App** → `html_apps/tv_clustered_stream.html`

---

**Last Updated:** 2025-09-30
**Status:** ✅ Fully Organized & Production Ready
