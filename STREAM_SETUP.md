# 🎬 Cloudflare Stream Setup Guide

## Step 1: Get Your API Token

### Option A: Use Existing Token (If You Have One)
```bash
export CLOUDFLARE_API_TOKEN='your_token_here'
```

### Option B: Create New API Token
1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Edit Cloudflare Stream" template OR create custom with:
   - **Permissions**: 
     - Account > Stream > Edit
   - **Account Resources**: 
     - Include > Your Account
4. Click "Continue to summary"
5. Click "Create Token"
6. **Copy the token** (you won't see it again!)

Then set it:
```bash
export CLOUDFLARE_API_TOKEN='your_new_token'
```

---

## Step 2: Upload Videos to Stream

```bash
# Upload all 593 videos (will take ~30-60 minutes)
python3 upload_to_stream.py
```

**What happens:**
- Uploads all videos from `channels_clustered/`
- Adds metadata (cluster name, channel info)
- Saves progress every 10 videos
- Creates `stream_upload_results.json` with all video IDs and URLs

**Expected time:** ~1 hour for 593 videos (with API rate limits)

---

## Step 3: Update Channel Config

```bash
# Generate new channels JSON with Stream URLs
python3 update_channels_with_stream.py
```

**Output:** `channels_clustered_stream.json`

---

## Step 4: Test Locally

**Option A: Use Stream-Specific HTML (Recommended)**
```bash
# Open the Stream-compatible version
open tv_clustered_stream.html
```

This version is specifically designed for Cloudflare Stream and uses iframe embeds.

**Option B: Modify Original HTML**
1. Edit `tv_clustered.html` line ~80:
   ```javascript
   // Change this:
   fetch('channels_clustered.json')
   
   // To this:
   fetch('channels_clustered_stream.json')
   ```

2. Open `tv_clustered.html` in browser
3. Videos should stream from Cloudflare!

---

## Step 5: Deploy to Cloudflare Pages

```bash
# Create public directory
mkdir -p public

# Copy Stream version (recommended)
cp tv_clustered_stream.html public/index.html
cp channels_clustered_stream.json public/channels_clustered_stream.json

# Or copy original version
# cp tv_clustered.html public/
# cp index.html public/
# cp channels_clustered_stream.json public/channels_clustered.json

# Deploy
wrangler pages deploy public --project-name interdimensional-cable
```

---

## 📊 View Analytics

After deployment, view your Stream analytics:
- **Dashboard**: https://dash.cloudflare.com/stream
- **Metrics**: Views, watch time, geographic distribution
- **Per-video**: Click any video to see detailed analytics

---

## 💰 Cost Estimate

**Your Setup:**
- 593 videos × 8 seconds = 79 minutes total
- Storage: $5/1,000 min = **$0.40/month**

**Delivery costs** (pay-as-you-go):
- $1 per 1,000 minutes watched
- 10 viewers watch all = $0.79
- 100 viewers watch all = $7.90

**Likely monthly cost: $1-8** for an art installation

---

## 🎨 Stream Player Features

**Automatic:**
- ✅ Adaptive bitrate streaming (adjusts to connection speed)
- ✅ Multiple quality levels encoded automatically
- ✅ Mobile optimization
- ✅ Thumbnail generation

**Analytics:**
- ✅ View counts
- ✅ Watch time
- ✅ Drop-off points
- ✅ Geographic distribution
- ✅ Device types

**Player Customization:**
- ✅ Can style to match your CRT aesthetic
- ✅ Custom controls
- ✅ Autoplay, loop, mute options
- ✅ No forced Cloudflare branding

---

## 🔧 Troubleshooting

### "API_TOKEN not found"
```bash
export CLOUDFLARE_API_TOKEN='your_token'
# Then run upload script again
```

### "Permission denied"
- Make sure token has "Stream > Edit" permission
- Token must be for the correct account

### Upload fails for some videos
- Check `stream_upload_progress.json` for completed uploads
- Re-run script - it will continue from where it left off
- Some videos may be blocked (aspect ratio, length, format issues)

### Videos not playing
- Check browser console for errors
- Ensure Stream URLs are correct in JSON
- Try iframe embed vs direct HLS playback

---

## 🚀 You're All Set!

Once deployed, your interdimensional cable TV will:
1. Stream videos from Cloudflare's global CDN
2. Automatically adjust quality for viewers
3. Track analytics on who's watching
4. Cost you ~$1-8/month for typical art installation traffic

Enjoy! 🎉
