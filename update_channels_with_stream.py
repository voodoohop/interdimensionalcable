#!/usr/bin/env python3
"""
Update channels_clustered.json with Cloudflare Stream URLs
Reads from stream_upload_results.json and updates the channel config
"""

import json
from pathlib import Path

def main():
    print("🔄 Updating channels_clustered.json with Stream URLs...")
    print("=" * 60)
    
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
    
    # Load existing channels config
    channels_file = 'channels_clustered.json'
    if not Path(channels_file).exists():
        print(f"❌ Error: {channels_file} not found!")
        return
    
    with open(channels_file, 'r') as f:
        channels = json.load(f)
    
    # Create mapping of original filename to Stream URL
    filename_to_stream = {}
    for result in successful:
        filename = result['filename']
        # Use iframe URL for embedding, or playback URL for HLS
        stream_url = result['iframe_url']  # Can also use 'playback_url' for HLS
        filename_to_stream[filename] = stream_url
    
    # Update channels
    updated_count = 0
    for channel in channels:
        for i, video in enumerate(channel['videos']):
            # Extract filename from path
            original_path = video['url']
            filename = original_path.split('/')[-1]
            
            if filename in filename_to_stream:
                # Update URL to Stream URL
                channel['videos'][i]['url'] = filename_to_stream[filename]
                updated_count += 1
    
    # Save updated channels
    output_file = 'channels_clustered_stream.json'
    with open(output_file, 'w') as f:
        json.dump(channels, f, indent=2)
    
    print(f"✅ Updated {updated_count} video URLs")
    print(f"💾 Saved to: {output_file}")
    print()
    print("📋 Next steps:")
    print("1. Test the new config locally:")
    print("   - Update tv_clustered.html to use 'channels_clustered_stream.json'")
    print("   - Open tv_clustered.html in browser")
    print("2. Deploy to Cloudflare Pages:")
    print("   - Copy tv_clustered.html, index.html, and channels_clustered_stream.json to public/")
    print("   - Run: wrangler pages deploy public --project-name interdimensional-cable")
    print()
    print("🎉 Your videos will now stream from Cloudflare Stream!")
    print("📊 View analytics: https://dash.cloudflare.com/stream")

if __name__ == '__main__':
    main()
