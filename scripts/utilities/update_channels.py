#!/usr/bin/env python3
"""
Simple script to update channels.json with current video files.
Run this whenever you add new channels or videos.
"""

import os
import json
from pathlib import Path

def update_channels():
    """Scan channels folder and update channels.json"""
    channels_dir = Path("channels")
    
    if not channels_dir.exists():
        print("Creating channels folder...")
        channels_dir.mkdir()
        print("Add your channel folders inside 'channels/' and run this script again.")
        return
    
    channels = []
    
    # Get all subdirectories in channels folder
    for channel_dir in sorted(channels_dir.iterdir()):
        if channel_dir.is_dir():
            # Use folder name as channel name (clean it up)
            channel_name = channel_dir.name.replace("_", " ").replace("-", " ")
            # Remove number prefixes like "01 " or "1. "
            if channel_name[0:3].replace(".", "").replace(" ", "").isdigit():
                channel_name = channel_name[3:].strip()
            
            # Get all video files
            videos = []
            for file in sorted(channel_dir.iterdir()):
                if file.suffix.lower() in ['.mp4', '.webm', '.mov', '.avi', '.mkv']:
                    videos.append(file.name)
            
            if videos:  # Only add if has videos
                channels.append({
                    "name": channel_name,
                    "folder": str(channel_dir),
                    "videos": videos
                })
    
    # Save to JSON
    with open("channels.json", "w") as f:
        json.dump({"channels": channels}, f, indent=2)
    
    print(f"✅ Updated channels.json with {len(channels)} channels:")
    for i, channel in enumerate(channels, 1):
        print(f"   {i}. {channel['name']} ({len(channel['videos'])} videos)")

if __name__ == "__main__":
    update_channels()
