# 🌊 Embedding Flow Viewer

An elegant video player that uses AI embeddings to create a seamless flow of similar content. Each video transitions to the most similar video based on CLIP embeddings, creating a natural, continuous viewing experience.

## Features

- **Smart Similarity**: Uses cosine similarity on CLIP embeddings to find the most similar next video
- **Watch History**: Tracks recently watched videos to avoid repetition
- **Smooth Flow**: Automatically plays the next most similar video when current one ends
- **Navigation**: Go back through your watch history or jump randomly
- **Vintage TV Aesthetic**: Same beautiful CRT-style interface as the clustered viewer

## Controls

- **← →** - Navigate through watch history (back/forward)
- **R** - Random jump to any video
- **F** - Toggle fullscreen
- **SPACE** - Play/Pause
- **Click** - Start with audio

## How It Works

1. All videos have pre-computed CLIP embeddings (512-dimensional vectors)
2. When a video ends, the system calculates cosine similarity between the current video's embedding and all other videos
3. The most similar video (that hasn't been watched recently) is selected and played
4. Similarity percentage is displayed to show how related videos are
5. Watch history allows you to navigate back through your viewing path

## Data Format

The viewer uses `video_embeddings_with_urls.json` which contains:
```json
{
  "videos": [
    {
      "filename": "video_name.mp4",
      "url": "https://cloudflare-stream-url/iframe",
      "embedding": [0.123, -0.456, ...] // 512-dim vector
    }
  ],
  "embedding_dim": 512,
  "total_videos": 894
}
```

## Generating Embeddings

To regenerate the embeddings JSON file:

```bash
python3 scripts/export_embeddings_to_json.py
```

This script:
1. Loads cached CLIP embeddings from `video_embeddings_cache/video_embeddings.pkl`
2. Matches videos with their Cloudflare Stream URLs
3. Exports to `video_embeddings_with_urls.json`

## Technical Details

- **Embedding Model**: CLIP ViT-B/32
- **Similarity Metric**: Cosine similarity
- **Recent History Size**: 20 videos (prevents loops)
- **Video Format**: HLS streaming via Cloudflare Stream
- **File Size**: ~13.4 MB JSON (894 videos × 512 dimensions)

## Comparison with Clustered Viewer

| Feature | Embedding Flow | Clustered Stream |
|---------|---------------|------------------|
| Organization | Dynamic similarity | Pre-defined channels |
| Navigation | Continuous flow | Channel switching |
| Variety | Gradual transitions | Cluster-based themes |
| Experience | Exploratory journey | Curated channels |

Both viewers offer unique experiences - use Embedding Flow for discovery and Clustered Stream for themed viewing!
