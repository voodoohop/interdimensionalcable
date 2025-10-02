# 🎬 Quick Reference - Video Import

## One-Line Commands

### Simple Import (Recommended)
```bash
python3 import_and_deploy_videos.py <source_dir> --prefix <name>
```

### With Semantic Reclustering
```bash
python3 import_and_deploy_videos.py <source_dir> --prefix <name> --recluster
```

### Dry Run (No Deploy)
```bash
python3 import_and_deploy_videos.py <source_dir> --prefix <name> --no-deploy
```

---

## Common Examples

```bash
# Import from generated_videos folder
python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels

# Import from Downloads with reclustering
python3 import_and_deploy_videos.py ~/Downloads/new_videos --prefix ale --recluster

# Test without deploying
python3 import_and_deploy_videos.py test_videos --prefix test --no-deploy

# Clean staging before import
python3 import_and_deploy_videos.py videos --prefix v1 --clean-staging
```

---

## What Each Option Does

| Option | Description |
|--------|-------------|
| `--prefix` | Tag for video filenames (e.g., `vkdels`, `ale`) |
| `--recluster` | Redistribute all videos by content similarity (slow) |
| `--no-deploy` | Preview changes without pushing to production |
| `--clean-staging` | Remove old files from staging directory |
| `--min-cluster-size N` | Minimum videos per cluster (default: 7) |

---

## Pipeline Steps

The script automatically runs:

1. **Import** → Copy videos with proper naming
2. **Upload** → Send to Cloudflare Stream
3. **Configure** → Add to channels or recluster
4. **Deploy** → Commit and push to GitHub

---

## Manual Steps (Advanced)

If you need more control:

```bash
# 1. Import
python3 scripts/utilities/import_new_videos.py <source> <staging> <prefix>

# 2. Upload
python3 scripts/stream_upload/upload_new_videos.py <staging>

# 3a. Add as new channel (fast)
python3 scripts/utilities/add_new_videos_to_channels.py

# 3b. OR recluster (slow)
python3 scripts/clustering/recluster_and_update_json.py

# 4. Deploy
git add channels_clustered_stream.json public/channels_clustered_stream.json
git commit -m "Add videos"
git push
```

---

## Troubleshooting

**Upload fails?**
- Check `api_keys.txt` has `CLOUDFLARE_API_TOKEN=...`
- Verify internet connection

**Reclustering too slow?**
- Skip `--recluster` flag
- Use `--min-cluster-size 10` for fewer clusters

**Need to test first?**
- Use `--no-deploy` flag
- Review changes before pushing

---

## Files to Know

- `import_and_deploy_videos.py` - Master pipeline
- `WORKFLOW.md` - Full documentation
- `channels_clustered_stream.json` - Channel configuration
- `video_embeddings_cache/` - Cached CLIP embeddings

---

## Quick Tips

✅ **First time?** Use simple import (no `--recluster`)  
✅ **Many videos?** Use `--recluster` for better organization  
✅ **Testing?** Always use `--no-deploy` first  
✅ **Clean start?** Use `--clean-staging`  
✅ **Custom prefix?** Use meaningful names like `runway`, `veo`, `ale`
