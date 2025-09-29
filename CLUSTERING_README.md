# Advanced Video Clustering System

Automatically discovers natural groupings in your video collection using CLIP embeddings and unsupervised machine learning.

## 🎯 What It Does

1. **Extracts frames** from all your videos (5 frames per video)
2. **Generates CLIP embeddings** - deep learning features that understand visual content
3. **Reduces dimensions** with UMAP (512 → 5 dimensions)
4. **Finds clusters** with HDBSCAN (discovers optimal number of groups)
5. **Visualizes** clusters in 2D space
6. **Reports** which videos belong together

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
./setup_clustering.sh
```

Or manually:
```bash
pip install torch torchvision
pip install git+https://github.com/openai/CLIP.git
pip install umap-learn hdbscan scikit-learn
pip install opencv-python pillow matplotlib seaborn tqdm
```

### Step 2: Run Clustering

```bash
# Complete analysis (embeddings + clustering + visualization + report)
python3 advanced_video_clusterer.py full

# Or step by step:
python3 advanced_video_clusterer.py analyze      # Compute embeddings & cluster
python3 advanced_video_clusterer.py visualize    # Create visualization
python3 advanced_video_clusterer.py report       # Export JSON report
python3 advanced_video_clusterer.py preview      # Preview reorganization
```

### Step 3: Review Results

- **`video_clusters_visualization.png`** - See your videos grouped by visual similarity
- **`cluster_analysis.json`** - Detailed breakdown of each cluster
- **`video_embeddings_cache/`** - Cached embeddings (reused on subsequent runs)

## 🎛️ Tuning Parameters

### Get More/Fewer Clusters

```bash
# More clusters (smaller groups)
python3 advanced_video_clusterer.py full --min-cluster-size 5

# Fewer clusters (larger groups)
python3 advanced_video_clusterer.py full --min-cluster-size 20
```

### Adjust Neighborhood Size

```bash
# Tighter clusters
python3 advanced_video_clusterer.py full --neighbors 10

# Looser clusters
python3 advanced_video_clusterer.py full --neighbors 25
```

### Force Recompute

```bash
# Recompute embeddings (if you added/removed videos)
python3 advanced_video_clusterer.py full --force
```

## 📊 Understanding Results

### Cluster Visualization
- Each **dot** = one video
- **Color** = cluster assignment
- **Proximity** = visual similarity
- **Gray dots** = outliers/noise (videos that don't fit clusters)

### Cluster Analysis JSON
```json
{
  "summary": {
    "total_videos": 694,
    "num_clusters": 12,
    "num_noise": 45
  },
  "clusters": {
    "cluster_0": {
      "size": 85,
      "channel_distribution": {
        "Chaotic_Harmony_Llama_Network": 45,
        "Melancholy_Toaster_Dreams": 40
      },
      "sample_videos": ["video1.mp4", "video2.mp4", ...]
    }
  }
}
```

## 💡 What Makes Good Clusters?

The system groups videos by **visual similarity**:
- **Color palette** (warm vs cool, bright vs dark)
- **Motion patterns** (static vs dynamic)
- **Subject matter** (abstract vs concrete)
- **Composition** (centered vs distributed)
- **Texture** (smooth vs detailed)

This is **more sophisticated** than keyword matching because it understands actual visual content.

## 🔄 Typical Workflow

1. **First run**: `python3 advanced_video_clusterer.py full`
   - Takes 5-10 minutes to process 694 videos
   - Creates embeddings cache

2. **Review results**: Check PNG visualization and JSON report

3. **Adjust if needed**: 
   ```bash
   python3 advanced_video_clusterer.py full --min-cluster-size 15
   ```

4. **Iterate**: Try different parameters until clusters make sense

5. **Optional**: Use Pollinations.ai to auto-name clusters (future feature)

## 🎨 Example Output

```
🔧 Loading CLIP model...
✅ CLIP model loaded on cpu
🔍 Scanning channels for videos...
✅ Found 694 videos across 15 channels
🎬 Computing CLIP embeddings for 694 videos...
⏱️  This may take 5-10 minutes...
Processing videos: 100%|████████| 694/694 [08:32<00:00, 1.35it/s]
✅ Computed embeddings for 694 videos (shape: (694, 512))

🔮 Clustering videos...
📊 Input: 694 videos with 512-dim embeddings
   🔸 UMAP: Reducing 512 → 5 dimensions...
   ✅ UMAP complete: (694, 5)
   🔸 HDBSCAN: Finding clusters (min_cluster_size=10)...
   🔸 Creating 2D visualization projection...

✅ Clustering complete!
   📊 Found 12 clusters
   🔇 45 videos marked as noise/outliers

📈 Cluster sizes:
   Cluster 0: 85 videos
   Cluster 1: 72 videos
   Cluster 2: 68 videos
   ...
```

## 🐛 Troubleshooting

### "No module named 'clip'"
```bash
pip install git+https://github.com/openai/CLIP.git
```

### "No module named 'umap'"
```bash
pip install umap-learn
```

### Too many/few clusters
Adjust `--min-cluster-size`:
- **Larger value** = fewer, bigger clusters
- **Smaller value** = more, smaller clusters

### Processing is slow
- Normal on CPU: ~1 video/second
- Much faster with GPU: ~10 videos/second
- Embeddings are cached, so only slow on first run

## 🎯 Next Steps

After clustering, you can:
1. Review which videos grouped together
2. Create new channel folders based on clusters
3. Move videos to reorganize your collection
4. Use cluster IDs as basis for new channel names
5. Optionally: Use Pollinations.ai vision API to generate semantic names for each cluster

---

**Built with:** CLIP (OpenAI) • UMAP • HDBSCAN • PyTorch
