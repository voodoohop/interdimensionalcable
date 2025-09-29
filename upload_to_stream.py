#!/usr/bin/env python3
"""
Cloudflare Stream Batch Upload Script
Uploads all videos from channels_clustered/ to Cloudflare Stream
"""

import os
import json
import requests
import time
from pathlib import Path
from typing import Dict, List

# Get Cloudflare credentials from environment or prompt
ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID', 'efdcb0933eaac64f27c0b295039b28f2')
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN', '')

if not API_TOKEN:
    print("⚠️  CLOUDFLARE_API_TOKEN not found in environment")
    print("Please set it using: export CLOUDFLARE_API_TOKEN='your_token_here'")
    print("\nOr get your API token from:")
    print("https://dash.cloudflare.com/profile/api-tokens")
    exit(1)

# Stream API endpoint
STREAM_API = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"

def upload_video(video_path: str, metadata: Dict) -> Dict:
    """Upload a single video to Cloudflare Stream"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    # Get video filename
    filename = os.path.basename(video_path)
    
    # Prepare multipart form data
    files = {
        'file': (filename, open(video_path, 'rb'), 'video/mp4')
    }
    
    # Add metadata
    data = {
        'meta': json.dumps(metadata)
    }
    
    print(f"📤 Uploading: {filename}...")
    
    try:
        response = requests.post(STREAM_API, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            video_id = result['result']['uid']
            playback_url = f"https://customer-{ACCOUNT_ID.replace('-', '')}.cloudflarestream.com/{video_id}/manifest/video.m3u8"
            iframe_url = f"https://customer-{ACCOUNT_ID.replace('-', '')}.cloudflarestream.com/{video_id}/iframe"
            
            print(f"   ✅ Uploaded! Video ID: {video_id}")
            return {
                'success': True,
                'video_id': video_id,
                'playback_url': playback_url,
                'iframe_url': iframe_url,
                'filename': filename,
                'metadata': metadata
            }
        else:
            print(f"   ❌ Failed: {result.get('errors', 'Unknown error')}")
            return {'success': False, 'filename': filename, 'error': result.get('errors')}
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {'success': False, 'filename': filename, 'error': str(e)}

def scan_videos(base_dir: str = 'channels_clustered') -> List[tuple]:
    """Scan all videos in channels_clustered directory"""
    videos = []
    base_path = Path(base_dir)
    
    for cluster_dir in sorted(base_path.iterdir()):
        if cluster_dir.is_dir() and cluster_dir.name.startswith(('0', '1', '2', '3')):
            cluster_name = cluster_dir.name
            cluster_number = cluster_name.split('_')[0]
            
            for video_file in sorted(cluster_dir.glob('*.mp4')):
                videos.append((str(video_file), cluster_name, cluster_number))
    
    return videos

def main():
    print("🎬 Cloudflare Stream Batch Upload")
    print("=" * 60)
    print(f"Account ID: {ACCOUNT_ID}")
    print()
    
    # Scan videos
    print("📂 Scanning videos...")
    videos = scan_videos()
    total_videos = len(videos)
    
    print(f"Found {total_videos} videos across {len(set(v[1] for v in videos))} clusters")
    print()
    
    # Confirm upload
    response = input(f"📤 Upload {total_videos} videos to Cloudflare Stream? (y/n): ")
    if response.lower() != 'y':
        print("❌ Upload cancelled")
        return
    
    print("\n🚀 Starting upload...")
    print("=" * 60)
    
    # Upload all videos
    results = []
    start_time = time.time()
    
    for idx, (video_path, cluster_name, cluster_number) in enumerate(videos, 1):
        filename = os.path.basename(video_path)
        
        # Create metadata
        metadata = {
            'cluster': cluster_name,
            'cluster_number': cluster_number,
            'original_filename': filename,
            'channel': f"Cluster {cluster_number}"
        }
        
        print(f"\n[{idx}/{total_videos}] {cluster_name}/{filename}")
        
        result = upload_video(video_path, metadata)
        results.append(result)
        
        # Rate limiting - small delay between uploads
        time.sleep(0.5)
        
        # Save progress every 10 videos
        if idx % 10 == 0:
            save_results(results, 'stream_upload_progress.json')
            elapsed = time.time() - start_time
            avg_time = elapsed / idx
            eta = avg_time * (total_videos - idx)
            print(f"\n⏱️  Progress: {idx}/{total_videos} | ETA: {int(eta/60)}m {int(eta%60)}s")
    
    # Save final results
    save_results(results, 'stream_upload_results.json')
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Upload Complete!")
    print("=" * 60)
    
    successful = sum(1 for r in results if r.get('success'))
    failed = total_videos - successful
    
    print(f"✅ Successful: {successful}/{total_videos}")
    print(f"❌ Failed: {failed}/{total_videos}")
    
    elapsed = time.time() - start_time
    print(f"⏱️  Total time: {int(elapsed/60)}m {int(elapsed%60)}s")
    
    if failed > 0:
        print(f"\n❌ Failed uploads:")
        for r in results:
            if not r.get('success'):
                print(f"   - {r.get('filename')}: {r.get('error')}")
    
    print(f"\n💾 Results saved to: stream_upload_results.json")
    print("\n📋 Next steps:")
    print("1. Run: python update_channels_with_stream.py")
    print("2. Deploy to Cloudflare Pages")
    print("3. View analytics at: https://dash.cloudflare.com/stream")

def save_results(results: List[Dict], filename: str):
    """Save upload results to JSON file"""
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total': len(results),
            'successful': sum(1 for r in results if r.get('success')),
            'failed': sum(1 for r in results if not r.get('success')),
            'results': results
        }, f, indent=2)

if __name__ == '__main__':
    main()
