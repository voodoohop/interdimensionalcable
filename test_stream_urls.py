#!/usr/bin/env python3
"""Quick test script to fetch a few Stream URLs and verify the fix works"""

import json
import os
import requests
import sys

# Get API token
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN', '')
if not API_TOKEN:
    print("❌ Error: CLOUDFLARE_API_TOKEN environment variable not set!")
    print("Run: export CLOUDFLARE_API_TOKEN='your_token'")
    sys.exit(1)

ACCOUNT_ID = 'efdcb0933eaac64f27c0b295039b28f2'

def get_stream_iframe_url(video_id: str) -> str:
    """Fetch the correct iframe URL from Cloudflare Stream API"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream/{video_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success') and 'result' in data:
            # Get the playback URL which contains the correct subdomain
            playback = data['result'].get('playback', {})
            hls_url = playback.get('hls', '')
            
            if hls_url:
                # Extract subdomain from HLS URL
                # Format: https://customer-XXXXX.cloudflarestream.com/VIDEO_ID/manifest/video.m3u8
                subdomain = hls_url.split('//')[1].split('.')[0]
                iframe_url = f"https://{subdomain}.cloudflarestream.com/{video_id}/iframe"
                return iframe_url
        
        print(f"⚠️  No playback URL for {video_id}")
        return None
        
    except Exception as e:
        print(f"❌ Error fetching {video_id}: {e}")
        return None

def main():
    print("🧪 Testing Stream URL fetch (5 videos)...\n")
    
    # Load upload results
    with open('stream_upload_results.json', 'r') as f:
        data = json.load(f)
    
    upload_results = data.get('results', [])
    successful_uploads = [u for u in upload_results if u.get('success')]
    print(f"📊 Found {len(successful_uploads)} successful uploads")
    print(f"🔍 Testing first 5 videos...\n")
    
    # Test first 5 videos
    test_videos = successful_uploads[:5]
    
    for i, upload in enumerate(test_videos, 1):
        video_id = upload['video_id']
        old_url = upload['iframe_url']
        
        print(f"{i}. Video ID: {video_id}")
        print(f"   Old URL: {old_url}")
        
        new_url = get_stream_iframe_url(video_id)
        
        if new_url:
            print(f"   New URL: {new_url}")
            if old_url != new_url:
                print(f"   ✅ URL CHANGED (this is good!)")
            else:
                print(f"   ⚠️  URL same (unexpected)")
        else:
            print(f"   ❌ Failed to fetch")
        print()
    
    print("✅ Test complete!")

if __name__ == '__main__':
    main()
