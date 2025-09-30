# 🎬 Runway UI Batch Download Guide

## Quick Steps to Download All Your Videos

### 1. Go to Your Assets
Open: https://app.runwayml.com/assets

### 2. Select All Videos
- **Mac**: Press `CMD + A`
- **PC**: Press `CTRL + A`

### 3. Download
1. A floating menu appears at the bottom of the screen
2. Click **Actions** dropdown
3. Select **Download**
4. Your videos will be compressed into a ZIP file
5. ZIP file will download to your computer

### 4. Extract the ZIP
- Extract to: `interdimensionalcable/runway_downloads/`

---

## 📝 Alternative: Select Specific Videos

### Select a Range
1. Click the **first video** you want
2. Hold **SHIFT**
3. Click the **last video** you want
4. Everything in between gets selected

### Select Individual Videos
1. Hold **CTRL** (PC) or **CMD** (Mac)
2. Click each video you want
3. Click **Actions** → **Download**

---

## ⚠️ Troubleshooting

### Download Doesn't Start?
**Problem**: Selection too large

**Solution**: Download in smaller batches
- Select 50-100 videos at a time
- Download each batch separately
- Repeat until all downloaded

### Can't Find Actions Menu?
**Make sure**: You have videos selected (they'll have a checkmark/highlight)

---

## 📊 After Downloading

Once you have the ZIP file extracted to `runway_downloads/`:

```bash
# Check what you downloaded
ls -lh runway_downloads/

# Count videos
ls runway_downloads/*.mp4 | wc -l

# See total size
du -sh runway_downloads/
```

---

## 🚀 Next: Upload to Cloudflare Stream

After downloading, upload to your streaming service:

```bash
python3 upload_to_stream.py runway_downloads/
```

This will upload all your Runway videos to Cloudflare Stream for the interdimensional cable project!
