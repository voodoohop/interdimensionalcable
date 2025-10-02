#!/usr/bin/env python3
"""
Import new videos into the project for clustering.
Copies videos from a source directory with proper naming conventions.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def sanitize_filename(filename):
    """Create a safe filename"""
    # Remove extension
    name = Path(filename).stem
    # Clean up WhatsApp naming
    name = name.replace('WhatsApp Video ', 'whatsapp_')
    name = name.replace(' at ', '_')
    name = name.replace('.', '_')
    name = name.replace(' ', '_')
    # Remove any remaining problematic characters
    safe_name = "".join(c for c in name if c.isalnum() or c in ('_', '-'))
    return safe_name

def import_videos(source_dir, output_dir='new_videos_staging', prefix='ale'):
    """Import videos from source directory"""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    
    # Find all video files
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
    video_files = [f for f in source_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in video_extensions]
    
    if not video_files:
        print(f"❌ No video files found in {source_dir}")
        return
    
    print(f"📁 Found {len(video_files)} videos in {source_dir}")
    print(f"📂 Output directory: {output_path.absolute()}")
    print()
    
    imported = 0
    skipped = 0
    
    for video_file in video_files:
        # Create new filename with prefix
        safe_name = sanitize_filename(video_file.name)
        new_filename = f"[{prefix}]_{safe_name}{video_file.suffix}"
        output_file = output_path / new_filename
        
        # Check if already exists
        if output_file.exists():
            print(f"⏭️  Skipped (exists): {new_filename}")
            skipped += 1
            continue
        
        # Copy file
        try:
            shutil.copy2(video_file, output_file)
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"✅ Imported: {new_filename} ({size_mb:.1f} MB)")
            imported += 1
        except Exception as e:
            print(f"❌ Failed to copy {video_file.name}: {e}")
    
    # Summary
    print()
    print("="*60)
    print("📊 Import Summary")
    print("="*60)
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📂 Output: {output_path.absolute()}")
    
    if imported > 0:
        print()
        print("🎯 Next Steps:")
        print("1. Review the imported videos in new_videos_staging/")
        print("2. Run clustering:")
        print(f"   python3 scripts/clustering/advanced_video_clusterer.py {output_dir}")
        print("3. Or add to existing channels manually")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 import_new_videos.py <source_directory> [output_dir] [prefix]")
        print()
        print("Example:")
        print("  python3 import_new_videos.py /Users/thomash/Downloads/alemorevids")
        print("  python3 import_new_videos.py ~/Downloads/videos new_videos ale")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'new_videos_staging'
    prefix = sys.argv[3] if len(sys.argv) > 3 else 'ale'
    
    import_videos(source_dir, output_dir, prefix)

if __name__ == '__main__':
    main()
