#!/usr/bin/env python3
"""
Prepare combined video collection for clustering with source metadata.
Creates symlinks with tagged filenames to preserve source information.
"""

import os
import json
from pathlib import Path
import shutil

def create_combined_collection():
    """Create a combined collection with source tags."""
    
    # Setup directories
    combined_dir = Path("videos_combined_for_clustering")
    existing_dir = Path("channels_clustered")
    new_dir = Path("new_videos_staging")
    
    # Clean and create combined directory
    if combined_dir.exists():
        print(f"🗑️  Removing existing {combined_dir}/")
        shutil.rmtree(combined_dir)
    
    combined_dir.mkdir()
    print(f"✅ Created {combined_dir}/")
    
    # Track metadata
    metadata = {
        'videos': [],
        'sources': {
            'existing': 0,
            'new': 0
        },
        'total': 0
    }
    
    # Process existing videos (tag as "existing")
    print(f"\n📦 Processing existing videos from {existing_dir}/...")
    existing_count = 0
    
    for cluster_dir in existing_dir.iterdir():
        if cluster_dir.is_dir() and not cluster_dir.name.startswith('.'):
            for video_file in cluster_dir.iterdir():
                if video_file.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                    # Create tagged filename: [existing]_originalname.mp4
                    tagged_name = f"[existing]_{video_file.name}"
                    target_path = combined_dir / tagged_name
                    
                    # Create symlink
                    os.symlink(video_file.resolve(), target_path)
                    
                    metadata['videos'].append({
                        'filename': tagged_name,
                        'original_path': str(video_file),
                        'source': 'existing',
                        'original_cluster': cluster_dir.name,
                        'size_mb': round(video_file.stat().st_size / (1024 * 1024), 2)
                    })
                    
                    existing_count += 1
    
    metadata['sources']['existing'] = existing_count
    print(f"✅ Linked {existing_count} existing videos")
    
    # Process new videos (preserve their source tags)
    print(f"\n📦 Processing new videos from {new_dir}/...")
    new_count = 0
    
    for video_file in new_dir.rglob('*'):
        if video_file.is_file() and video_file.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
            # Extract source tag from filename (e.g., "glitchy_", "afrofuture_")
            filename = video_file.name
            
            # Determine source from filename prefix
            source_tag = "new"
            if filename.startswith("glitchy_"):
                source_tag = "glitchy_tokyo"
            elif filename.startswith("afrofuture_"):
                source_tag = "afrofuture"
            elif filename.startswith("whatsapp_"):
                source_tag = "whatsapp"
            elif filename.startswith("id_"):
                source_tag = "id_samples"
            elif filename.startswith("turbo_"):
                source_tag = "turbo_gen"
            elif filename.startswith("documents_"):
                source_tag = "documents"
            elif filename.startswith("morina_"):
                source_tag = "morina"
            elif filename.startswith("japan_"):
                source_tag = "japan_afro"
            elif filename.startswith("web_"):
                source_tag = "web_ui"
            
            # Create tagged filename: [source]_originalname.mp4
            tagged_name = f"[{source_tag}]_{filename}"
            target_path = combined_dir / tagged_name
            
            # Create symlink
            os.symlink(video_file.resolve(), target_path)
            
            metadata['videos'].append({
                'filename': tagged_name,
                'original_path': str(video_file),
                'source': source_tag,
                'size_mb': round(video_file.stat().st_size / (1024 * 1024), 2)
            })
            
            new_count += 1
    
    metadata['sources']['new'] = new_count
    metadata['total'] = existing_count + new_count
    print(f"✅ Linked {new_count} new videos")
    
    # Save metadata
    metadata_file = combined_dir / "video_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Combined collection ready!")
    print(f"   📊 Total videos: {metadata['total']}")
    print(f"   📦 Existing: {existing_count}")
    print(f"   🆕 New: {new_count}")
    print(f"   📝 Metadata saved to: {metadata_file}")
    print(f"\n🎯 Next step: Run clustering on {combined_dir}/")
    
    return metadata

if __name__ == "__main__":
    metadata = create_combined_collection()
    
    print("\n" + "="*60)
    print("🚀 READY TO CLUSTER!")
    print("="*60)
    print("\nRun clustering with:")
    print("  python3 advanced_video_clusterer.py videos_combined_for_clustering \\")
    print("    --min-cluster-size 7 \\")
    print("    --output-dir channels_reclustered_all")
    print("\nThis will create fresh clusters with source tags preserved in filenames!")
