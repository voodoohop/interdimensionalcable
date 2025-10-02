#!/usr/bin/env python3
"""
Add new videos to existing embeddings and re-cluster everything.
This avoids re-computing embeddings for all existing videos.
"""

import os
import sys
import pickle
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Import the clusterer
sys.path.insert(0, str(Path(__file__).parent))
from advanced_video_clusterer import VideoClusterer

def add_new_videos_and_recluster(new_videos_dir, cache_dir="video_embeddings_cache", 
                                  output_dir="channels_clustered", min_cluster_size=7):
    """
    Add new videos to existing embeddings and re-cluster.
    
    Args:
        new_videos_dir: Directory containing new videos to add
        cache_dir: Directory with cached embeddings
        output_dir: Where to save clustered channels
        min_cluster_size: Minimum cluster size for HDBSCAN
    """
    
    cache_file = Path(cache_dir) / "video_embeddings.pkl"
    new_videos_path = Path(new_videos_dir)
    
    # Load existing embeddings
    if not cache_file.exists():
        print(f"❌ No cached embeddings found at {cache_file}")
        print("   Run advanced_video_clusterer.py first to create initial embeddings")
        return
    
    print("📦 Loading existing embeddings...")
    with open(cache_file, 'rb') as f:
        cached_data = pickle.load(f)
        existing_videos = cached_data['video_files']
        existing_embeddings = cached_data['embeddings']
    
    print(f"✅ Loaded {len(existing_videos)} existing videos")
    
    # Find new videos
    if not new_videos_path.exists():
        print(f"❌ New videos directory not found: {new_videos_dir}")
        return
    
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
    new_video_files = [f for f in new_videos_path.iterdir() 
                       if f.is_file() and f.suffix.lower() in video_extensions]
    
    if not new_video_files:
        print(f"❌ No video files found in {new_videos_dir}")
        return
    
    print(f"\n📹 Found {len(new_video_files)} new videos")
    
    # Initialize clusterer for computing new embeddings
    clusterer = VideoClusterer()
    
    # Compute embeddings for new videos
    print(f"\n🎬 Computing embeddings for {len(new_video_files)} new videos...")
    new_embeddings = []
    new_video_infos = []
    
    for video_file in tqdm(new_video_files, desc="Processing new videos"):
        embedding = clusterer.compute_video_embedding(str(video_file))
        if embedding is not None:
            new_embeddings.append(embedding)
            new_video_infos.append({
                'path': video_file,
                'name': video_file.name,
                'channel': video_file.parent.name,
                'size_mb': video_file.stat().st_size / (1024 * 1024)
            })
    
    if not new_embeddings:
        print("❌ Failed to compute embeddings for new videos")
        return
    
    new_embeddings = np.array(new_embeddings)
    print(f"✅ Computed {len(new_embeddings)} new embeddings")
    
    # Combine embeddings
    print(f"\n🔗 Combining embeddings...")
    all_embeddings = np.vstack([existing_embeddings, new_embeddings])
    all_videos = existing_videos + new_video_infos
    
    print(f"✅ Total: {len(all_videos)} videos ({len(existing_videos)} existing + {len(new_video_infos)} new)")
    
    # Update cache with combined embeddings
    print(f"\n💾 Updating cache...")
    with open(cache_file, 'wb') as f:
        pickle.dump({
            'video_files': all_videos,
            'embeddings': all_embeddings
        }, f)
    print(f"✅ Cache updated")
    
    # Set the embeddings in the clusterer
    clusterer.video_files = all_videos
    clusterer.embeddings = all_embeddings
    
    # Run clustering
    print(f"\n🔮 Clustering {len(all_videos)} videos (min_cluster_size={min_cluster_size})...")
    labels = clusterer.cluster_videos(min_cluster_size=min_cluster_size)
    
    if labels is None:
        print("❌ Clustering failed")
        return
    
    # Save clusters using reorganize function
    print(f"\n💾 Saving clusters to {output_dir}...")
    from reorganize_by_clusters import reorganize_videos
    reorganize_videos(clusterer, output_dir=output_dir, mode='copy')
    
    # Generate summary
    print("\n" + "="*60)
    print("📊 Clustering Summary")
    print("="*60)
    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"✅ Total videos: {len(all_videos)}")
    print(f"   - Existing: {len(existing_videos)}")
    print(f"   - New: {len(new_video_infos)}")
    print(f"📺 Channels created: {n_clusters}")
    print(f"🔇 Unclustered (noise): {n_noise}")
    print(f"📂 Output: {Path(output_dir).absolute()}")
    
    print("\n🎯 Next Steps:")
    print("1. Review the clusters in", output_dir)
    print("2. Upload to Cloudflare Stream:")
    print("   python3 scripts/stream_upload/upload_to_stream.py")
    print("3. Update channel config:")
    print("   python3 scripts/stream_upload/update_channels_with_stream.py")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Add new videos and re-cluster')
    parser.add_argument('new_videos_dir', help='Directory with new videos to add')
    parser.add_argument('--cache-dir', default='video_embeddings_cache', 
                       help='Cache directory (default: video_embeddings_cache)')
    parser.add_argument('--output-dir', default='channels_clustered',
                       help='Output directory (default: channels_clustered)')
    parser.add_argument('--min-cluster-size', type=int, default=7,
                       help='Minimum cluster size (default: 7)')
    
    args = parser.parse_args()
    
    add_new_videos_and_recluster(
        args.new_videos_dir,
        args.cache_dir,
        args.output_dir,
        args.min_cluster_size
    )

if __name__ == '__main__':
    main()
