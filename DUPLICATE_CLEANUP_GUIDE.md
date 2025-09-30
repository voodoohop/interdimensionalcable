# 🧹 Duplicate Upload Cleanup Guide

## Problem Identified

**Issue**: The upload script was tracking uploads by **filename only**, not full path. Since the same filename can exist in different cluster folders, it re-uploaded videos multiple times.

**Current Status**:
- 894 unique videos in `channels_reclustered_all/`
- 1,462+ uploads to Cloudflare Stream
- **~568 duplicate uploads** wasting storage

---

## ✅ What's Been Fixed

### 1. Upload Script (`upload_to_stream.py`)
**Changes**:
- Now tracks uploads by **full file path** instead of just filename
- Stores `full_path` in progress file for accurate deduplication
- Backward compatible with old progress files

### 2. Cleanup Script (`cleanup_duplicates.py`)
**Purpose**: Delete duplicate videos from Cloudflare Stream

**Features**:
- Identifies duplicates by filename
- Keeps the FIRST upload of each video
- Deletes all subsequent duplicates
- Creates cleaned progress file

---

## 📋 Cleanup Steps

### Step 1: Stop Current Upload
```bash
# Press Ctrl+C in the terminal running the upload
^C
```

### Step 2: Run Duplicate Cleanup
```bash
# Source your environment variables
source .env

# Run cleanup script
python3 cleanup_duplicates.py
```

**What it does**:
1. Analyzes `docs/stream_upload_progress.json`
2. Identifies ~568 duplicate videos
3. Shows examples and asks for confirmation
4. Deletes duplicates from Cloudflare Stream
5. Creates `docs/stream_upload_progress_cleaned.json`

### Step 3: Replace Progress File
```bash
# Backup old progress
mv docs/stream_upload_progress.json docs/stream_upload_progress_backup.json

# Use cleaned version
mv docs/stream_upload_progress_cleaned.json docs/stream_upload_progress.json
```

### Step 4: Resume Upload (if needed)
```bash
# The fixed script will now properly skip already-uploaded videos
bash run_upload.sh
```

---

## 💰 Cost Impact

**Duplicate Storage**:
- ~568 duplicate videos
- Average size: ~5-10 MB per video
- Estimated waste: **~3-6 GB of duplicate storage**

**Cloudflare Stream Pricing**:
- Storage: $5/1000 minutes
- Estimated duplicate cost: **~$10-20/month** (depending on video length)

**After Cleanup**: You'll only pay for 894 unique videos

---

## 🔍 Verification

After cleanup, verify the counts:

```bash
# Check cleaned progress file
cat docs/stream_upload_progress.json | jq '.successful'
# Should show: 894

# Count actual videos
find channels_reclustered_all -type f \( -name "*.mp4" -o -name "*.webm" -o -name "*.mov" \) | wc -l
# Should show: 894

# They should match!
```

---

## 🚀 Next Steps After Cleanup

1. **Verify Upload Complete**:
   ```bash
   python3 -c "
   import json
   with open('docs/stream_upload_progress.json') as f:
       data = json.load(f)
       print(f'Uploaded: {data[\"successful\"]}/894')
   "
   ```

2. **Generate Stream-based Channels Config**:
   ```bash
   python3 update_channels_with_stream.py
   ```

3. **Test TV App**:
   ```bash
   python3 -m http.server 8000
   # Visit: http://localhost:8000/tv_clustered_stream.html
   ```

4. **Deploy to Production**

---

## 🛡️ Prevention

The fixed `upload_to_stream.py` now:
- ✅ Tracks by full file path (not just filename)
- ✅ Stores `full_path` in progress file
- ✅ Properly deduplicates across cluster folders
- ✅ Shows accurate progress counts

**This won't happen again!**

---

## 📊 Summary

| Metric | Before | After Cleanup |
|--------|--------|---------------|
| Total Videos | 894 | 894 |
| Stream Uploads | 1,462+ | 894 |
| Duplicates | 568+ | 0 |
| Storage Waste | ~3-6 GB | 0 |
| Monthly Cost | Extra $10-20 | Normal |

---

## ⚠️ Important Notes

1. **Current Upload Running**: Let it finish or stop it - doesn't matter, cleanup will handle it
2. **Backup**: The old progress file is saved as `stream_upload_progress_backup.json`
3. **Cloudflare API**: Cleanup uses DELETE API - make sure your token has permissions
4. **Rate Limits**: Cleanup script deletes with reasonable pacing

---

## 🆘 Troubleshooting

### "Permission denied" during cleanup
- Check your `CLOUDFLARE_API_TOKEN` has Stream edit permissions

### Cleanup script fails partway through
- It's safe to re-run - it will skip already-deleted videos
- Check the cleaned progress file for what was completed

### Want to manually verify duplicates
```bash
python3 -c "
import json
from collections import Counter

with open('docs/stream_upload_progress.json') as f:
    data = json.load(f)
    
filenames = [r['filename'] for r in data['results'] if r.get('success')]
dupes = {k: v for k, v in Counter(filenames).items() if v > 1}

print(f'Duplicate filenames: {len(dupes)}')
for name, count in sorted(dupes.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f'  {name}: {count} times')
"
```

---

**Status**: ✅ Ready to clean up duplicates and save money!
