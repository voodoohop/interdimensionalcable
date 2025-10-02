#!/usr/bin/env python3
"""
Simple script to upload new videos from a directory to Cloudflare Stream
"""

import os
import json
import requests
from pathlib import Path

# Cloudflare credentials
ACCOUNT_ID = 'efdcb0933eaac64f27c0b295039b28f2'
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN', '')

if not API_TOKEN:
    # Try to read from api_keys.txt
    try:
        with open('api_keys.txt', 'r') as f:
            for line in f:
                if 'CLOUDFLARE_API_TOKEN' in line:
                    API_TOKEN = line.split('=')[1].strip()
                    break
    except:
        pass

if not API_TOKEN:
    print("❌ CLOUDFLARE_API_TOKEN not found")
    exit(1)

STREAM_API = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"

def upload_video(video_path):
    """Upload a single video to Cloudflare Stream"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    filename = os.path.basename(video_path)
    
    files = {
        'file': (filename, open(video_path, 'rb'), 'video/mp4')
    }
    
    data = {
        'meta': json.dumps({'name': filename})
    }
    
    print(f"📤 Uploading: {filename}...")
    
    try:
        response = requests.post(STREAM_API, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            video_id = result['result']['uid']
            playback_url = f"https://customer-{ACCOUNT_ID.replace('-', '')}.cloudflarestream.com/{video_id}/manifest/video.m3u8"
            
            print(f"   ✅ Success! Video ID: {video_id}")
            print(f"   🔗 Playback URL: {playback_url}")
            
            return {
                'success': True,
                'filename': filename,
                'video_id': video_id,
                'playback_url': playback_url
            }
        else:
            print(f"   ❌ Failed: {result.get('errors')}")
            return {'success': False, 'filename': filename, 'error': result.get('errors')}
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {'success': False, 'filename': filename, 'error': str(e)}

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 upload_new_videos.py <directory>")
        print("Example: python3 upload_new_videos.py new_videos_staging")
        exit(1)
    
    video_dir = Path(sys.argv[1])
    
    if not video_dir.exists():
        print(f"❌ Directory not found: {video_dir}")
        exit(1)
    
    # Find all video files
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
    videos = [f for f in video_dir.iterdir() 
              if f.is_file() and f.suffix.lower() in video_extensions]
    
    if not videos:
        print(f"❌ No video files found in {video_dir}")
        exit(1)
    
    print(f"🎬 Found {len(videos)} videos to upload")
    print("=" * 60)
    
    results = []
    for video in videos:
        result = upload_video(str(video))
        results.append(result)
        print()
    
    # Summary
    print("=" * 60)
    print("📊 Upload Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r.get('success'))
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {len(results) - successful}/{len(results)}")
    
    # Save results
    output_file = 'docs/new_videos_upload_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")

if __name__ == '__main__':
    main()
