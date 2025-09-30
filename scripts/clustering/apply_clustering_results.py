#!/usr/bin/env python3
"""
Apply clustering results to create new channel structure.
Uses the cluster_analysis.json to organize videos with source tags preserved.
"""

import json
import shutil
from pathlib import Path
from collections import defaultdict

def apply_clustering():
    """Create new channel structure from clustering results."""
    
    # Load clustering results
    print("📊 Loading clustering results...")
    with open('cluster_analysis.json', 'r') as f:
        analysis = json.load(f)
    
    # Setup directories
    output_dir = Path("channels_reclustered_all")
    source_dir = Path("videos_combined_for_clustering_wrapped/all_videos")
    
    # Clean output directory
    if output_dir.exists():
        print(f"🗑️  Removing existing {output_dir}/")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir()
    print(f"✅ Created {output_dir}/")
    
    # Track statistics
    stats = {
        'total_videos': analysis['summary']['total_videos'],
        'num_clusters': analysis['summary']['num_clusters'],
        'videos_organized': 0,
        'source_distribution': defaultdict(int)
    }
    
    print(f"\n🎬 Organizing {stats['total_videos']} videos into {stats['num_clusters']} channels...\n")
    
    for cluster_id, cluster_data in analysis['clusters'].items():
        # Create cluster folder with padded number
        # Extract number from "cluster_0" format
        cluster_num = int(cluster_id.replace('cluster_', ''))
        cluster_name = f"{cluster_num+1:02d}_Cluster_{cluster_num}"
        cluster_path = output_dir / cluster_name
        cluster_path.mkdir()
        
        # Copy videos to cluster folder
        video_count = 0
        for video_name in cluster_data['sample_videos']:
            source_path = source_dir / video_name
            
            if source_path.exists():
                # Copy with original tagged name
                dest_path = cluster_path / video_name
                shutil.copy2(source_path, dest_path)
                video_count += 1
                stats['videos_organized'] += 1
                
                # Track source distribution
                if video_name.startswith('[existing]'):
                    stats['source_distribution']['existing'] += 1
                elif video_name.startswith('[glitchy_tokyo]'):
                    stats['source_distribution']['glitchy_tokyo'] += 1
                elif video_name.startswith('[afrofuture]'):
                    stats['source_distribution']['afrofuture'] += 1
                elif video_name.startswith('[whatsapp]'):
                    stats['source_distribution']['whatsapp'] += 1
                elif video_name.startswith('[id_samples]'):
                    stats['source_distribution']['id_samples'] += 1
                else:
                    stats['source_distribution']['other'] += 1
        
        print(f"✅ {cluster_name}: {video_count} videos")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"🎉 REORGANIZATION COMPLETE!")
    print(f"{'='*60}")
    print(f"\n📊 Statistics:")
    print(f"   • Total videos organized: {stats['videos_organized']}/{stats['total_videos']}")
    print(f"   • Channels created: {stats['num_clusters']}")
    print(f"\n📦 Source Distribution:")
    for source, count in sorted(stats['source_distribution'].items(), key=lambda x: -x[1]):
        percentage = (count / stats['videos_organized']) * 100
        print(f"   • {source}: {count} videos ({percentage:.1f}%)")
    
    print(f"\n✅ New channel structure ready in: {output_dir}/")
    print(f"\n🎯 Next steps:")
    print(f"   1. Review the new channel organization")
    print(f"   2. Run: python3 update_channels.py (to generate channels.json)")
    print(f"   3. Test with tv_app.html")
    print(f"   4. Upload to Cloudflare Stream if satisfied")
    
    return stats

if __name__ == "__main__":
    stats = apply_clustering()
