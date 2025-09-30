#!/usr/bin/env python3
"""
Update channels.json for the clustered video channels.
Run this to generate the channel configuration for the TV interface.
"""

import os
import json
from pathlib import Path

def update_clustered_channels():
    """Scan channels_clustered folder and update channels_clustered.json"""
    channels_dir = Path("channels_clustered")
    
    if not channels_dir.exists():
        print("❌ channels_clustered folder not found!")
        print("Run the clustering script first: python3 reorganize_by_clusters.py --mode copy")
        return
    
    channels = []
    
    # Get all subdirectories in channels_clustered folder
    for channel_dir in sorted(channels_dir.iterdir()):
        if channel_dir.is_dir():
            # Extract cluster number from folder name (e.g., "cluster_00" -> "Cluster 00")
            channel_name = channel_dir.name.replace("_", " ").title()
            
            # Get all video files
            videos = []
            for file in sorted(channel_dir.iterdir()):
                if file.suffix.lower() in ['.mp4', '.webm', '.mov', '.avi', '.mkv']:
                    videos.append(file.name)
            
            if videos:  # Only add if has videos
                channels.append({
                    "name": channel_name,
                    "folder": str(channel_dir),
                    "videos": videos,
                    "video_count": len(videos)
                })
    
    # Save to JSON
    output_file = "channels_clustered.json"
    with open(output_file, "w") as f:
        json.dump({"channels": channels}, f, indent=2)
    
    print(f"✅ Updated {output_file} with {len(channels)} clustered channels:")
    for i, channel in enumerate(channels, 1):
        print(f"   {i}. {channel['name']} ({len(channel['videos'])} videos)")
    print(f"\n📺 Open tv_clustered.html in your browser to view!")

if __name__ == "__main__":
    update_clustered_channels()
