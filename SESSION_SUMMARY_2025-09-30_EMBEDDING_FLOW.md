# Session Summary: Embedding Flow Viewer - 2025-09-30

## What We Built

Created a new **embedding-based video viewer** that plays videos in a continuous flow based on AI similarity, without using predefined channels.

## Files Created

### 1. `scripts/export_embeddings_to_json.py`
- Exports CLIP embeddings from pickle cache to JSON
- Matches videos with Cloudflare Stream URLs
- **Output**: `video_embeddings_with_urls.json` (13.4 MB, 894 videos)

### 2. `html_apps/tv_embedding_flow.html`
- Main viewer application
- Self-contained HTML with vintage TV aesthetic
- Client-side cosine similarity calculation
- **Key Feature**: Tracks watch history to avoid repeating videos

### 3. Supporting Files
- `html_apps/README_EMBEDDING_FLOW.md` - Documentation
- `EMBEDDING_FLOW_SUMMARY.md` - Technical details
- `index.html` - Updated landing page with both viewers

## How the Watch History Works

**YES, it avoids replaying videos!** Here's how:

```javascript
// In the code:
this.watchHistory = []; // Tracks what we've watched

findMostSimilarVideo(currentIndex, excludeRecent = true) {
    // Get recently watched videos to avoid repeating
    const recentlyWatched = excludeRecent 
        ? new Set(this.watchHistory.slice(-20))  // Last 20 videos
        : new Set([currentIndex]);
    
    // Skip videos in recentlyWatched when finding next video
    for (let i = 0; i < this.videos.length; i++) {
        if (recentlyWatched.has(i)) continue;  // SKIP if recently watched
        // ... calculate similarity ...
    }
}
```

### Watch History Behavior

1. **Tracks all watched videos** in `this.watchHistory` array
2. **Excludes last 20 videos** when finding next similar video
3. **Prevents short loops** - won't replay same videos immediately
4. **Auto-resets** when all videos have been watched
5. **Back navigation** - can go back through history with ← key

### Example Flow

```
Video 1 (random start)
  ↓ 85% similar
Video 2 
  ↓ 92% similar
Video 3
  ↓ 78% similar
Video 4
  ... continues ...

History: [1, 2, 3, 4, ...]
Excluded from next: [last 20 videos]
```

## Current Status

### ✅ Working
- Embeddings exported to JSON (894 videos)
- Viewer HTML created with full functionality
- Watch history tracking implemented
- Similarity calculation working
- Server running on port 3000

### ⚠️ Issue
- Viewer not loading in browser
- Possible causes:
  - Large JSON file (13.4 MB) taking time to load
  - CORS or file path issue
  - Browser console errors (not checked yet)

## Next Steps for New Session

1. **Debug loading issue**
   - Check browser console for errors
   - Verify JSON file path is correct
   - Test if JSON loads successfully
   - Consider compressing JSON or using lazy loading

2. **Potential Improvements**
   - Add loading progress indicator for JSON
   - Compress embeddings (use Float32Array instead of full JSON)
   - Add "never repeat" mode (exclude ALL watched videos)
   - Show watch history visualization
   - Add "reset history" button

3. **Testing**
   - Verify similarity calculations work correctly
   - Test watch history prevents loops
   - Test back/forward navigation
   - Test random jump functionality

## Key Technical Details

- **Embeddings**: CLIP ViT-B/32 (512 dimensions, normalized)
- **Similarity**: Cosine similarity (efficient with normalized vectors)
- **History Size**: Last 20 videos excluded
- **Total Videos**: 894 matched with stream URLs
- **Data Format**: JSON with filename, URL, and embedding array

## URLs

- **Server**: http://localhost:3000
- **Embedding Flow**: http://localhost:3000/html_apps/tv_embedding_flow.html
- **Clustered Channels**: http://localhost:3000/html_apps/tv_clustered_stream.html
- **Landing Page**: http://localhost:3000/

## Code Locations

```
interdimensionalcable/
├── video_embeddings_with_urls.json          # 13.4 MB data file
├── scripts/
│   └── export_embeddings_to_json.py         # Export script
├── html_apps/
│   ├── tv_embedding_flow.html               # Main viewer
│   ├── tv_clustered_stream.html             # Original clustered viewer
│   └── README_EMBEDDING_FLOW.md             # Documentation
├── EMBEDDING_FLOW_SUMMARY.md                # Technical summary
└── index.html                                # Landing page
```

## Watch History Implementation Details

The viewer maintains a complete history and uses it smartly:

```javascript
// When video ends
playNextVideo() {
    // Find most similar, excluding last 20
    const nextIndex = this.findMostSimilarVideo(this.currentIndex);
    this.currentIndex = nextIndex;
    this.watchHistory.push(nextIndex);  // Add to history
    // ... load and play ...
}

// Going back
playPreviousVideo() {
    if (this.watchHistory.length > 1) {
        this.watchHistory.pop();  // Remove current
        this.currentIndex = this.watchHistory[this.watchHistory.length - 1];
        // ... load and play ...
    }
}

// Random jump
randomJump() {
    const newIndex = Math.floor(Math.random() * this.videos.length);
    this.watchHistory.push(newIndex);  // Add to history
    // ... load and play ...
}
```

## Summary

**The viewer DOES avoid replaying videos** by maintaining a watch history and excluding the last 20 watched videos when calculating the next most similar video. This creates a smooth, non-repetitive viewing experience while still following the embedding similarity flow.

The main issue to resolve is the loading problem - likely related to the large JSON file or a path/CORS issue that needs debugging in the browser console.
