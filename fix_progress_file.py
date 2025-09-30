#!/usr/bin/env python3
"""
Fix progress file by removing orphaned uploads and keeping only current videos
"""

import json
import os
from pathlib import Path

def main():
    print("🔧 Fixing Upload Progress File")
    print("=" * 60)
    
    # Get all actual video files currently in channels_reclustered_all
    print("📂 Scanning current video files...")
    actual_files = set()
    for root, dirs, files in os.walk('channels_reclustered_all'):
        for file in files:
            if file.lower().endswith(('.mp4', '.webm', '.mov', '.avi', '.mkv')):
                actual_files.add(file)
    
    print(f"Found {len(actual_files)} actual video files")
    
    # Load progress file
    print("\n📥 Loading progress file...")
    with open('docs/stream_upload_progress.json') as f:
        data = json.load(f)
    
    original_count = len(data['results'])
    successful_count = sum(1 for r in data['results'] if r.get('success'))
    
    print(f"Progress file has {original_count} total entries")
    print(f"  - {successful_count} successful uploads")
    
    # Filter to only keep uploads for files that still exist
    print("\n🧹 Removing orphaned uploads...")
    cleaned_results = []
    orphaned_count = 0
    
    for result in data['results']:
        if result.get('success'):
            filename = result['filename']
            if filename in actual_files:
                cleaned_results.append(result)
            else:
                orphaned_count += 1
        else:
            # Keep failed uploads for reference
            cleaned_results.append(result)
    
    print(f"Removed {orphaned_count} orphaned uploads")
    print(f"Kept {len(cleaned_results)} relevant entries")
    
    # Create cleaned data
    cleaned_data = {
        'timestamp': data.get('timestamp', ''),
        'total': len(cleaned_results),
        'successful': sum(1 for r in cleaned_results if r.get('success')),
        'failed': sum(1 for r in cleaned_results if not r.get('success')),
        'results': cleaned_results
    }
    
    # Save cleaned version
    print("\n💾 Saving cleaned progress file...")
    with open('docs/stream_upload_progress_fixed.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"Actual video files: {len(actual_files)}")
    print(f"Successfully uploaded (current): {cleaned_data['successful']}")
    print(f"Still need to upload: {len(actual_files) - cleaned_data['successful']}")
    print(f"Orphaned uploads removed: {orphaned_count}")
    
    print("\n✅ Fixed progress saved to: docs/stream_upload_progress_fixed.json")
    print("\n📋 Next steps:")
    print("1. Stop current upload (Ctrl+C)")
    print("2. Backup old: mv docs/stream_upload_progress.json docs/stream_upload_progress_old.json")
    print("3. Use fixed: mv docs/stream_upload_progress_fixed.json docs/stream_upload_progress.json")
    print("4. Re-run upload with fixed script")

if __name__ == '__main__':
    main()
