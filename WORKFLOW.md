# 🎬 Interdimensional Cable - Video Import Workflow

## Quick Start

### Simple Import (Recommended for most cases)
Add videos as a new channel without reclustering:

```bash
python3 import_and_deploy_videos.py <source_directory> --prefix <prefix>
```

**Example:**
```bash
python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels
```

### Semantic Reclustering (Better organization, slower)
Redistribute all videos based on content similarity:

```bash
python3 import_and_deploy_videos.py <source_directory> --prefix <prefix> --recluster
```

**Example:**
```bash
python3 import_and_deploy_videos.py ~/Downloads/new_videos --prefix ale --recluster
```

---

## What the Pipeline Does

1. **Import** - Copies videos from source directory with proper naming (`[prefix]_filename.mp4`)
2. **Upload** - Uploads to Cloudflare Stream and gets video IDs
3. **Configure** - Either:
   - Adds videos to a new channel (fast)
   - OR semantically reclusters all videos (slow but better)
4. **Deploy** - Commits and pushes to GitHub (auto-deploys to live site)

---

## Options

```bash
python3 import_and_deploy_videos.py <source_directory> [OPTIONS]

Required:
  source_directory          Directory containing videos to import

Optional:
  --prefix PREFIX           Prefix for video filenames (default: video)
  --staging-dir DIR         Staging directory (default: new_videos_staging)
  --recluster               Semantically recluster all videos
  --min-cluster-size N      Minimum cluster size (default: 7)
  --no-deploy               Don't commit/push (dry run)
  --clean-staging           Clean staging directory before import
```

---

## Manual Workflow (Advanced)

If you need more control, run steps individually:

### Step 1: Import Videos
```bash
python3 scripts/utilities/import_new_videos.py <source_directory> [staging_dir] [prefix]
```

### Step 2: Upload to Cloudflare Stream
```bash
python3 scripts/stream_upload/upload_new_videos.py <staging_directory>
```

### Step 3a: Add as New Channel (Fast)
```bash
python3 scripts/utilities/add_new_videos_to_channels.py
```

### Step 3b: Semantic Reclustering (Slow)
```bash
python3 scripts/clustering/recluster_and_update_json.py --min-cluster-size 7
```

### Step 4: Deploy
```bash
git add channels_clustered_stream.json public/channels_clustered_stream.json
git commit -m "Add new videos"
git push origin main
```

---

## Environment Setup

### Required
- Python 3.11+
- Cloudflare API Token (in `api_keys.txt` or `CLOUDFLARE_API_TOKEN` env var)

### Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
- `torch` - For CLIP embeddings
- `transformers` - CLIP model
- `umap-learn` - Dimensionality reduction
- `hdbscan` - Clustering
- `requests` - API calls
- `tqdm` - Progress bars

---

## File Structure

```
interdimensionalcable/
├── import_and_deploy_videos.py          # Master pipeline script
├── WORKFLOW.md                          # This file
├── scripts/
│   ├── utilities/
│   │   ├── import_new_videos.py         # Import & rename videos
│   │   └── add_new_videos_to_channels.py # Add to new channel
│   ├── stream_upload/
│   │   └── upload_new_videos.py         # Upload to Cloudflare
│   └── clustering/
│       ├── recluster_and_update_json.py # Semantic reclustering
│       └── advanced_video_clusterer.py  # Core clustering logic
├── channels_clustered_stream.json       # Main channel config
├── public/
│   └── channels_clustered_stream.json   # Public channel config
└── video_embeddings_cache/
    └── video_embeddings.pkl             # Cached CLIP embeddings
```

---

## Troubleshooting

### "No such file or directory" errors
- Make sure source directory exists and contains video files
- Check that video files have valid extensions (.mp4, .mov, .avi, .mkv, .webm)

### "CLOUDFLARE_API_TOKEN not found"
- Add token to `api_keys.txt`: `CLOUDFLARE_API_TOKEN=your_token_here`
- Or set environment variable: `export CLOUDFLARE_API_TOKEN=your_token`

### Upload fails
- Check internet connection
- Verify Cloudflare API token is valid
- Check Cloudflare Stream quota

### Reclustering takes too long
- Use simple import instead (skip `--recluster`)
- Reduce `--min-cluster-size` to create fewer, larger clusters
- Reclustering processes all videos (~5-10 minutes for 1000+ videos)

---

## Tips

- **First time?** Use simple import without `--recluster`
- **Many similar videos?** Use `--recluster` to organize by content
- **Testing?** Use `--no-deploy` to preview changes
- **Clean start?** Use `--clean-staging` to remove old staging files
- **Custom prefix?** Use meaningful prefixes like `ale`, `vkdels`, `runway`

---

## Examples

```bash
# Quick import of generated videos
python3 import_and_deploy_videos.py generated_videos/batch1 --prefix gen1

# Import and recluster for better organization
python3 import_and_deploy_videos.py ~/Downloads/videos --prefix downloads --recluster

# Dry run (don't deploy)
python3 import_and_deploy_videos.py test_videos --prefix test --no-deploy

# Clean staging and import
python3 import_and_deploy_videos.py new_batch --prefix batch2 --clean-staging

# Custom cluster size
python3 import_and_deploy_videos.py videos --prefix v1 --recluster --min-cluster-size 10
```
