#!/usr/bin/env python3
"""
Update channels_clustered.json with Cloudflare Stream URLs
Fetches correct playback URLs from Cloudflare Stream API
"""

import json
import os
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

ACCOUNT_ID = 'efdcb0933eaac64f27c0b295039b28f2'

def get_correct_stream_url(video_id, api_token):
    """Fetch the correct iframe URL from Cloudflare Stream API"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream/{video_id}"
    headers = {'Authorization': f'Bearer {api_token}'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success') and 'result' in data:
            result = data['result']
            # Get the HLS URL and convert to iframe format
            if 'playback' in result and 'hls' in result['playback']:
                hls_url = result['playback']['hls']
                # Extract the correct subdomain from HLS URL
                # Format: https://customer-XXXXX.cloudflarestream.com/VIDEO_ID/manifest/video.m3u8
                base_url = hls_url.split('/manifest/')[0]
                iframe_url = f"{base_url}/iframe"
                return iframe_url
    except Exception as e:
        print(f"⚠️  Error fetching URL for {video_id}: {e}")
    
    return None

def main():
    print("🔄 Updating channels_clustered.json with correct Stream URLs...")
    print("=" * 60)
    
    # Get API token
    api_token = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not api_token:
        print("❌ Error: CLOUDFLARE_API_TOKEN environment variable not set!")
        print("Run: export CLOUDFLARE_API_TOKEN='your_token'")
        return
    
    # Load Stream upload results
    results_file = 'stream_upload_results.json'
    if not Path(results_file).exists():
        print(f"❌ Error: {results_file} not found!")
        print("Please run upload_to_stream.py first")
        return
    
    with open(results_file, 'r') as f:
        upload_data = json.load(f)
    
    results = upload_data['results']
    successful = [r for r in results if r.get('success')]
    
    print(f"📊 Loaded {len(successful)} successful uploads")
    print(f"🔍 Fetching correct playback URLs from API...")
    
    # Load existing channels config
    channels_file = 'channels_clustered.json'
    if not Path(channels_file).exists():
        print(f"❌ Error: {channels_file} not found!")
        return
    
    with open(channels_file, 'r') as f:
        channels_data = json.load(f)
    
    # Handle both formats: {"channels": [...]} or [...]
    if isinstance(channels_data, dict) and 'channels' in channels_data:
        channels = channels_data['channels']
    else:
        channels = channels_data
    
    # Create mapping of original filename to correct Stream URL using parallel processing
    filename_to_stream = {}
    print(f"   Fetching URLs in parallel (20 threads)...")
    print(f"   This should take ~60-90 seconds for {len(successful)} videos...")
    
    # Thread-safe counter for progress
    progress_lock = threading.Lock()
    processed_count = [0]
    
    def fetch_url(result):
        """Fetch URL for a single video"""
        filename = result['filename']
        video_id = result['video_id']
        correct_url = get_correct_stream_url(video_id, api_token)
        
        with progress_lock:
            processed_count[0] += 1
            if processed_count[0] % 50 == 0:
                print(f"   Processed {processed_count[0]}/{len(successful)} videos... ({processed_count[0]*100//len(successful)}%)")
        
        return (filename, correct_url)
    
    # Process in parallel with 20 threads (gentler on API)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_url, result) for result in successful]
        
        for future in as_completed(futures):
            try:
                filename, correct_url = future.result()
                if correct_url:
                    filename_to_stream[filename] = correct_url
            except Exception as e:
                print(f"⚠️  Error: {e}")
    
    print(f"✅ Fetched {len(filename_to_stream)} correct URLs")
    
    # Update channels - convert filename strings to objects with URLs
    updated_count = 0
    for channel in channels:
        new_videos = []
        for video in channel['videos']:
            # Video is just a filename string
            filename = video if isinstance(video, str) else video.get('url', '').split('/')[-1]
            
            if filename in filename_to_stream:
                # Create video object with Stream URL
                new_videos.append({
                    'filename': filename,
                    'url': filename_to_stream[filename]
                })
                updated_count += 1
            else:
                print(f"⚠️  No Stream URL found for: {filename}")
        
        channel['videos'] = new_videos
    
    # Save updated channels (preserve original format)
    output_file = 'channels_clustered_stream.json'
    if isinstance(channels_data, dict) and 'channels' in channels_data:
        output_data = {'channels': channels}
    else:
        output_data = channels
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Updated {updated_count} video URLs")
    print(f"💾 Saved to: {output_file}")
    print()
    print("📋 Next steps:")
    print("1. Test the new config locally:")
    print("   - Update tv_clustered_stream.html line 233 to use 'channels_clustered_stream.json'")
    print("   - Run: python3 -m http.server 8000")
    print("   - Open: http://localhost:8000/tv_clustered_stream.html")
    print("2. Deploy to Cloudflare Pages:")
    print("   rm -rf public && mkdir public")
    print("   cp tv_clustered_stream.html public/index.html")
    print("   cp channels_clustered_stream.json public/")
    print("   wrangler pages deploy public --project-name interdimensional-cable --commit-dirty=true")
    print()
    print("🎉 Your videos will now stream from Cloudflare Stream!")
    print("📊 View analytics: https://dash.cloudflare.com/stream")

if __name__ == '__main__':
    main()
