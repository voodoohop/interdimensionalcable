#!/usr/bin/env python3
"""
Recluster all videos using cached embeddings and update the JSON configuration.
This works with already-uploaded videos on Cloudflare Stream.
"""

import os
import sys
import json
import pickle
import numpy as np
from pathlib import Path
from collections import defaultdict

# Import the clusterer
sys.path.insert(0, str(Path(__file__).parent))
from advanced_video_clusterer import VideoClusterer

def recluster_and_update_json(cache_file="video_embeddings_cache/video_embeddings.pkl",
                               channels_json="channels_clustered_stream.json",
                               upload_results="docs/new_videos_upload_results.json",
                               min_cluster_size=7):
    """
    Recluster videos using cached embeddings and update JSON configuration.
    
    Args:
        cache_file: Path to cached embeddings
        channels_json: Path to channels JSON file
        upload_results: Path to upload results JSON
        min_cluster_size: Minimum cluster size for HDBSCAN
    """
    
    # Load existing embeddings
    cache_path = Path(cache_file)
    if not cache_path.exists():
        print(f"❌ No cached embeddings found at {cache_file}")
        return
    
    print("📦 Loading cached embeddings...")
    with open(cache_path, 'rb') as f:
        cached_data = pickle.load(f)
        video_files = cached_data['video_files']
        embeddings = cached_data['embeddings']
    
    print(f"✅ Loaded {len(video_files)} videos with embeddings")
    
    # Load existing channels to get video URLs
    print("\n📺 Loading existing channel configuration...")
    with open(channels_json, 'r') as f:
        channels_data = json.load(f)
    
    # Create a mapping of filename to URL from existing channels
    filename_to_url = {}
    for channel in channels_data['channels']:
        for video in channel['videos']:
            filename_to_url[video['filename']] = video['url']
    
    print(f"✅ Found {len(filename_to_url)} videos in existing channels")
    
    # Load upload results for new videos
    if Path(upload_results).exists():
        print("\n📤 Loading upload results for new videos...")
        with open(upload_results, 'r') as f:
            upload_data = json.load(f)
        
        # Add new videos to filename_to_url mapping
        for video in upload_data:
            if video.get('success'):
                video_id = video['video_id']
                iframe_url = f"https://customer-8l6qnv6y72wms6uk.cloudflarestream.com/{video_id}/iframe"
                filename_to_url[video['filename']] = iframe_url
        
        print(f"✅ Added {len(upload_data)} newly uploaded videos")
    
    # Initialize clusterer
    clusterer = VideoClusterer()
    clusterer.video_files = video_files
    clusterer.embeddings = embeddings
    
    # Run clustering
    print(f"\n🔮 Clustering {len(video_files)} videos (min_cluster_size={min_cluster_size})...")
    labels = clusterer.cluster_videos(min_cluster_size=min_cluster_size)
    
    if labels is None:
        print("❌ Clustering failed")
        return
    
    # Organize videos by cluster
    print("\n📊 Organizing videos by cluster...")
    clusters = defaultdict(list)
    noise_videos = []
    
    for idx, (video_info, label) in enumerate(zip(video_files, labels)):
        video_name = video_info['name']
        
        # Find matching URL
        video_url = None
        for filename, url in filename_to_url.items():
            # Match by filename (handle different prefixes)
            if video_name in filename or filename in video_name:
                video_url = url
                break
        
        if video_url is None:
            print(f"⚠️  No URL found for: {video_name}")
            continue
        
        video_entry = {
            "filename": video_name,
            "url": video_url
        }
        
        if label == -1:
            noise_videos.append(video_entry)
        else:
            clusters[label].append(video_entry)
    
    # Create new channels structure
    print("\n🎬 Creating new channel structure...")
    new_channels = []
    
    # Sort clusters by size (largest first)
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
    
    for channel_num, (cluster_id, videos) in enumerate(sorted_clusters, 1):
        channel = {
            "name": f"{channel_num:02d} Semantic Channel {cluster_id}",
            "videos": videos
        }
        new_channels.append(channel)
    
    # Add noise videos as a separate channel if any
    if noise_videos:
        new_channels.append({
            "name": f"{len(new_channels) + 1:02d} Unclustered",
            "videos": noise_videos
        })
    
    # Update channels data
    channels_data['channels'] = new_channels
    
    # Save updated channels
    print(f"\n💾 Saving updated channels...")
    with open(channels_json, 'w') as f:
        json.dump(channels_data, f, indent=2)
    
    # Also update public version
    public_file = 'public/channels_clustered_stream.json'
    with open(public_file, 'w') as f:
        json.dump(channels_data, f, indent=2)
    
    # Generate summary
    print("\n" + "="*60)
    print("📊 Reclustering Summary")
    print("="*60)
    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    n_noise = list(labels).count(-1)
    
    print(f"✅ Total videos: {len(video_files)}")
    print(f"📺 Semantic channels: {n_clusters}")
    print(f"🔇 Unclustered: {n_noise}")
    print(f"📝 Updated: {channels_json}")
    print(f"📝 Updated: {public_file}")
    
    print("\n🎯 Next Steps:")
    print("1. Test locally: open html_apps/tv_clustered_stream.html")
    print("2. Commit and push:")
    print(f"   git add {channels_json} {public_file}")
    print('   git commit -m "Recluster all videos semantically"')
    print("   git push origin main")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Recluster videos and update JSON')
    parser.add_argument('--cache-file', default='video_embeddings_cache/video_embeddings.pkl',
                       help='Path to cached embeddings')
    parser.add_argument('--channels-json', default='channels_clustered_stream.json',
                       help='Path to channels JSON file')
    parser.add_argument('--upload-results', default='docs/new_videos_upload_results.json',
                       help='Path to upload results JSON')
    parser.add_argument('--min-cluster-size', type=int, default=7,
                       help='Minimum cluster size (default: 7)')
    
    args = parser.parse_args()
    
    recluster_and_update_json(
        args.cache_file,
        args.channels_json,
        args.upload_results,
        args.min_cluster_size
    )

if __name__ == '__main__':
    main()
