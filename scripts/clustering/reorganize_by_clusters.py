#!/usr/bin/env python3
"""
Reorganize videos into new channel folders based on clustering results.
Creates a parallel folder structure in channels_clustered/
"""

import os
import shutil
import json
import pickle
import numpy as np
from pathlib import Path
from collections import defaultdict
import argparse
from tqdm import tqdm

# Import clustering from main script
from advanced_video_clusterer import VideoClusterer


def reorganize_videos(clusterer, output_dir="channels_clustered", mode='copy'):
    """
    Reorganize videos into cluster-based channels.
    
    Args:
        clusterer: VideoClusterer instance with computed clusters
        output_dir: Directory for new channel structure
        mode: 'copy' or 'move' videos
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"🎬 REORGANIZING {len(clusterer.video_files)} VIDEOS INTO CLUSTERS")
    print(f"{'='*80}\n")
    
    # Get unique clusters (excluding noise)
    unique_clusters = sorted(set(clusterer.cluster_labels))
    num_clusters = len([c for c in unique_clusters if c >= 0])
    num_noise = np.sum(clusterer.cluster_labels == -1)
    
    print(f"📊 Summary:")
    print(f"   • Total videos: {len(clusterer.video_files)}")
    print(f"   • Clusters: {num_clusters}")
    print(f"   • Noise/outliers: {num_noise}")
    print(f"   • Output directory: {output_dir}")
    print(f"   • Mode: {mode}\n")
    
    # Create a folder for each cluster
    cluster_stats = {}
    
    for cluster_id in tqdm(unique_clusters, desc="Creating cluster folders"):
        if cluster_id == -1:
            folder_name = f"00_Uncategorized"
        else:
            folder_name = f"{cluster_id+1:02d}_Cluster_{cluster_id}"
        
        cluster_path = output_path / folder_name
        cluster_path.mkdir(exist_ok=True)
        
        # Get videos in this cluster
        mask = clusterer.cluster_labels == cluster_id
        cluster_videos = [clusterer.video_files[i] for i in np.where(mask)[0]]
        
        # Analyze channel distribution
        channel_dist = defaultdict(int)
        for video in cluster_videos:
            channel_dist[video['channel']] += 1
        
        # Copy/move videos
        copied_count = 0
        for video in cluster_videos:
            source = video['path']
            dest = cluster_path / video['name']
            
            try:
                if mode == 'copy':
                    if not dest.exists():
                        shutil.copy2(source, dest)
                        copied_count += 1
                else:  # move
                    if not dest.exists():
                        shutil.move(str(source), str(dest))
                        copied_count += 1
            except Exception as e:
                print(f"❌ Error processing {video['name']}: {e}")
        
        # Store stats
        cluster_stats[folder_name] = {
            'cluster_id': int(cluster_id),
            'size': int(len(cluster_videos)),
            'files_processed': int(copied_count),
            'channel_distribution': {k: int(v) for k, v in sorted(channel_dist.items(), key=lambda x: -x[1])[:5]},
            'sample_videos': [v['name'] for v in cluster_videos[:5]]
        }
    
    # Save reorganization report
    report_path = output_path / "reorganization_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            'summary': {
                'total_videos': int(len(clusterer.video_files)),
                'num_clusters': int(num_clusters),
                'num_noise': int(num_noise),
                'mode': mode
            },
            'clusters': cluster_stats
        }, f, indent=2)
    
    print(f"\n✅ Reorganization complete!")
    print(f"📁 New structure: {output_dir}/")
    print(f"📄 Report saved: {report_path}")
    
    # Print summary
    print(f"\n📊 Cluster Summary:")
    for folder_name, stats in sorted(cluster_stats.items()):
        top_channel = list(stats['channel_distribution'].items())[0] if stats['channel_distribution'] else ('N/A', 0)
        print(f"   {folder_name}: {stats['size']} videos (top: {top_channel[0]}: {top_channel[1]})")
    
    return cluster_stats


def main():
    parser = argparse.ArgumentParser(description="Reorganize videos by clustering")
    parser.add_argument("--output-dir", default="channels_clustered",
                       help="Output directory for clustered channels")
    parser.add_argument("--mode", choices=['copy', 'move'], default='copy',
                       help="Copy or move videos (default: copy)")
    parser.add_argument("--min-cluster-size", type=int, default=30,
                       help="Minimum cluster size for re-clustering (default: 30)")
    parser.add_argument("--recluster", action="store_true",
                       help="Re-run clustering with new parameters")
    parser.add_argument("--preview", action="store_true",
                       help="Preview reorganization without copying files")
    
    args = parser.parse_args()
    
    # Load clusterer
    print("🔧 Loading clustering results...")
    clusterer = VideoClusterer()
    clusterer.compute_all_embeddings()
    
    if args.recluster:
        print(f"\n🔄 Re-clustering with min_cluster_size={args.min_cluster_size}...")
        clusterer.cluster_videos(min_cluster_size=args.min_cluster_size)
        clusterer.visualize_clusters(save_path=f"video_clusters_size{args.min_cluster_size}.png")
        clusterer.export_cluster_report(output_file=f"cluster_analysis_size{args.min_cluster_size}.json")
    else:
        print("📦 Using cached clustering results...")
        clusterer.cluster_videos(min_cluster_size=10)  # Will load from cache
    
    if args.preview:
        # Just show what would happen
        print(f"\n🔍 PREVIEW MODE - No files will be copied")
        print(f"\nWould create {len(set(clusterer.cluster_labels))} folders in {args.output_dir}/")
        
        for cluster_id in sorted(set(clusterer.cluster_labels)):
            mask = clusterer.cluster_labels == cluster_id
            count = np.sum(mask)
            if cluster_id == -1:
                print(f"   00_Uncategorized: {count} videos")
            else:
                print(f"   {cluster_id+1:02d}_Cluster_{cluster_id}: {count} videos")
    else:
        # Actually reorganize
        reorganize_videos(clusterer, output_dir=args.output_dir, mode=args.mode)
        
        print(f"\n💡 Next steps:")
        print(f"   1. Review the new folders in {args.output_dir}/")
        print(f"   2. Rename cluster folders to meaningful names")
        print(f"   3. Run: python3 update_channels.py (update channels.json)")
        print(f"   4. Update tv_app.html to point to new channels folder")


if __name__ == "__main__":
    main()
