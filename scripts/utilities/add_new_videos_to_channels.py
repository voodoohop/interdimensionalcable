#!/usr/bin/env python3
"""
Add newly uploaded videos to channels configuration
"""

import json
from pathlib import Path

def add_new_videos_to_channels():
    # Load new videos upload results
    new_videos_file = 'docs/new_videos_upload_results.json'
    channels_file = 'channels_clustered_stream.json'
    
    with open(new_videos_file, 'r') as f:
        new_videos = json.load(f)
    
    with open(channels_file, 'r') as f:
        channels_data = json.load(f)
    
    # Convert playback URLs to iframe URLs
    new_channel_videos = []
    for video in new_videos:
        if video.get('success'):
            # Extract video ID from playback URL
            video_id = video['video_id']
            # Create iframe URL (matching existing format)
            iframe_url = f"https://customer-8l6qnv6y72wms6uk.cloudflarestream.com/{video_id}/iframe"
            
            new_channel_videos.append({
                "filename": video['filename'],
                "url": iframe_url
            })
    
    # Add as a new channel
    new_channel = {
        "name": f"{len(channels_data['channels']) + 1:02d} Ale's New Videos",
        "videos": new_channel_videos
    }
    
    channels_data['channels'].append(new_channel)
    
    # Save updated channels
    with open(channels_file, 'w') as f:
        json.dump(channels_data, f, indent=2)
    
    # Also update public version
    public_file = 'public/channels_clustered_stream.json'
    with open(public_file, 'w') as f:
        json.dump(channels_data, f, indent=2)
    
    print(f"✅ Added {len(new_channel_videos)} videos to new channel")
    print(f"📺 Total channels: {len(channels_data['channels'])}")
    print(f"📝 Updated: {channels_file}")
    print(f"📝 Updated: {public_file}")
    print(f"\n🎯 Next steps:")
    print("1. Test locally: open html_apps/tv_clustered_stream.html")
    print("2. Commit and push to deploy")

if __name__ == '__main__':
    add_new_videos_to_channels()
