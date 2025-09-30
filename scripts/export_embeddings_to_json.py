#!/usr/bin/env python3
"""
Export video embeddings to JSON format with stream URLs for the embedding-based viewer.
"""

import pickle
import json
import numpy as np
from pathlib import Path

def load_embeddings():
    """Load embeddings from pickle cache."""
    cache_file = Path("video_embeddings_cache/video_embeddings.pkl")
    with open(cache_file, 'rb') as f:
        data = pickle.load(f)
    return data['video_files'], data['embeddings']

def load_stream_urls():
    """Load stream URLs from channels_clustered_stream.json."""
    with open('channels_clustered_stream.json', 'r') as f:
        data = json.load(f)
    
    # Create a mapping from filename to stream URL
    url_map = {}
    for channel in data['channels']:
        for video in channel['videos']:
            filename = video['filename']
            url_map[filename] = video['url']
    
    return url_map

def export_embeddings_json():
    """Export embeddings with stream URLs to JSON."""
    print("📦 Loading embeddings...")
    video_files, embeddings = load_embeddings()
    
    print("🔗 Loading stream URLs...")
    url_map = load_stream_urls()
    
    print("🔄 Matching videos to stream URLs...")
    
    # Build the output data
    videos_data = []
    matched = 0
    unmatched = 0
    
    for i, video_info in enumerate(video_files):
        filename = video_info['name']
        
        # Try to find matching stream URL
        stream_url = url_map.get(filename)
        
        if stream_url:
            videos_data.append({
                'filename': filename,
                'url': stream_url,
                'embedding': embeddings[i].tolist()  # Convert numpy array to list
            })
            matched += 1
        else:
            unmatched += 1
            print(f"⚠️  No stream URL found for: {filename}")
    
    print(f"\n✅ Matched {matched} videos with stream URLs")
    print(f"⚠️  {unmatched} videos without stream URLs")
    
    # Save to JSON
    output_file = 'video_embeddings_with_urls.json'
    print(f"\n💾 Saving to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump({
            'videos': videos_data,
            'embedding_dim': embeddings.shape[1],
            'total_videos': len(videos_data)
        }, f, indent=2)
    
    print(f"✅ Exported {len(videos_data)} videos with embeddings to {output_file}")
    print(f"📊 File size: {Path(output_file).stat().st_size / (1024*1024):.2f} MB")

if __name__ == '__main__':
    export_embeddings_json()
