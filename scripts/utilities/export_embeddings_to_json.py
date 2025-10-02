#!/usr/bin/env python3
"""
Export video embeddings cache to JSON format for embedding flow visualization.
"""

import json
import pickle
import numpy as np
from pathlib import Path

def export_embeddings_to_json():
    """Export embeddings from pickle cache to JSON with URLs from channels config"""
    
    # Load embeddings cache
    cache_file = Path('video_embeddings_cache/video_embeddings.pkl')
    if not cache_file.exists():
        print(f"❌ Cache file not found: {cache_file}")
        return
    
    print("📦 Loading embeddings cache...")
    with open(cache_file, 'rb') as f:
        cached_data = pickle.load(f)
        video_files = cached_data['video_files']
        embeddings = cached_data['embeddings']
    
    print(f"✅ Loaded {len(video_files)} videos with embeddings")
    
    # Load channels config to get URLs
    channels_file = Path('channels_clustered_stream.json')
    if not channels_file.exists():
        print(f"❌ Channels file not found: {channels_file}")
        return
    
    print("📺 Loading channel configuration...")
    with open(channels_file, 'r') as f:
        channels_data = json.load(f)
    
    # Create filename to URL mapping
    filename_to_url = {}
    for channel in channels_data['channels']:
        for video in channel['videos']:
            filename_to_url[video['filename']] = video['url']
    
    print(f"✅ Found {len(filename_to_url)} videos in channels")
    
    # Build output data
    output_videos = []
    matched = 0
    unmatched = 0
    
    for idx, (video_info, embedding) in enumerate(zip(video_files, embeddings)):
        video_name = video_info['name']
        
        # Find matching URL
        video_url = None
        for filename, url in filename_to_url.items():
            if video_name in filename or filename in video_name:
                video_url = url
                break
        
        if video_url:
            output_videos.append({
                "name": video_name,
                "url": video_url,
                "embedding": embedding.tolist()
            })
            matched += 1
        else:
            unmatched += 1
            if unmatched <= 5:  # Show first 5 unmatched
                print(f"⚠️  No URL found for: {video_name}")
    
    # Create output structure
    output_data = {
        "videos": output_videos,
        "embedding_dim": embeddings.shape[1],
        "total_videos": len(output_videos)
    }
    
    # Save to both root and public
    output_file = Path('video_embeddings_with_urls.json')
    public_file = Path('public/video_embeddings_with_urls.json')
    
    print(f"\n💾 Saving embeddings...")
    with open(output_file, 'w') as f:
        json.dump(output_data, f)
    
    with open(public_file, 'w') as f:
        json.dump(output_data, f)
    
    # Summary
    print("\n" + "="*60)
    print("📊 Export Summary")
    print("="*60)
    print(f"✅ Matched videos: {matched}")
    print(f"⚠️  Unmatched videos: {unmatched}")
    print(f"📐 Embedding dimension: {embeddings.shape[1]}")
    print(f"📝 Saved to: {output_file}")
    print(f"📝 Saved to: {public_file}")
    print(f"💾 File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
    
    print("\n🎯 Embedding flow HTML is now updated!")
    print("   Test: open html_apps/tv_embedding_flow.html")

if __name__ == '__main__':
    export_embeddings_to_json()
