#!/usr/bin/env python3
"""
Clean up duplicate video uploads from Cloudflare Stream
"""

import os
import json
import requests
from pathlib import Path
from collections import defaultdict

# Get credentials
ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID', 'efdcb0933eaac64f27c0b295039b28f2')
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN', '')

if not API_TOKEN:
    print("⚠️  CLOUDFLARE_API_TOKEN not found")
    exit(1)

STREAM_API = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"

def delete_video(video_id: str) -> bool:
    """Delete a video from Cloudflare Stream"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"{STREAM_API}/{video_id}"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json().get('success', False)
    except Exception as e:
        print(f"   ❌ Error deleting {video_id}: {e}")
        return False

def main():
    print("🧹 Cloudflare Stream Duplicate Cleanup")
    print("=" * 60)
    
    # Load progress file
    progress_file = 'docs/stream_upload_progress.json'
    with open(progress_file, 'r') as f:
        data = json.load(f)
    
    results = data['results']
    successful = [r for r in results if r.get('success')]
    
    print(f"Total uploads in progress file: {len(successful)}")
    
    # Group by filename - keep only the FIRST upload of each
    seen_filenames = {}
    duplicates_to_delete = []
    
    for result in successful:
        filename = result['filename']
        video_id = result['video_id']
        
        if filename in seen_filenames:
            # This is a duplicate - mark for deletion
            duplicates_to_delete.append({
                'filename': filename,
                'video_id': video_id,
                'original_id': seen_filenames[filename]
            })
        else:
            # First occurrence - keep it
            seen_filenames[filename] = video_id
    
    print(f"Unique videos: {len(seen_filenames)}")
    print(f"Duplicates to delete: {len(duplicates_to_delete)}")
    print()
    
    if len(duplicates_to_delete) == 0:
        print("✅ No duplicates found!")
        return
    
    # Show some examples
    print("Example duplicates:")
    for dup in duplicates_to_delete[:5]:
        print(f"  - {dup['filename']}")
        print(f"    Keep: {dup['original_id']}")
        print(f"    Delete: {dup['video_id']}")
    print()
    
    # Confirm deletion
    response = input(f"🗑️  Delete {len(duplicates_to_delete)} duplicate videos? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cleanup cancelled")
        return
    
    print("\n🚀 Deleting duplicates...")
    print("=" * 60)
    
    deleted_count = 0
    failed_count = 0
    
    for i, dup in enumerate(duplicates_to_delete, 1):
        print(f"[{i}/{len(duplicates_to_delete)}] Deleting {dup['filename'][:50]}...")
        
        if delete_video(dup['video_id']):
            deleted_count += 1
            print(f"   ✅ Deleted")
        else:
            failed_count += 1
            print(f"   ❌ Failed")
        
        # Progress update every 50
        if i % 50 == 0:
            print(f"\n⏱️  Progress: {i}/{len(duplicates_to_delete)} | Deleted: {deleted_count} | Failed: {failed_count}\n")
    
    print("\n" + "=" * 60)
    print("📊 Cleanup Complete!")
    print("=" * 60)
    print(f"✅ Deleted: {deleted_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"💾 Kept: {len(seen_filenames)} unique videos")
    
    # Create cleaned progress file
    cleaned_results = [r for r in successful if r['filename'] in seen_filenames and r['video_id'] == seen_filenames[r['filename']]]
    
    cleaned_data = {
        'timestamp': data['timestamp'],
        'total': len(cleaned_results),
        'successful': len(cleaned_results),
        'failed': 0,
        'results': cleaned_results
    }
    
    with open('docs/stream_upload_progress_cleaned.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"\n💾 Cleaned progress saved to: docs/stream_upload_progress_cleaned.json")
    print("\n📋 Next steps:")
    print("1. Stop the current upload (Ctrl+C)")
    print("2. Replace progress file: mv docs/stream_upload_progress_cleaned.json docs/stream_upload_progress.json")
    print("3. Re-run upload with fixed script")

if __name__ == '__main__':
    main()
