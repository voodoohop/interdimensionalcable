#!/usr/bin/env python3
"""
Advanced Video Clustering using CLIP Embeddings
Automatically discovers natural groupings in your video collection.
"""

import os
import cv2
import json
import torch
import clip
import numpy as np
from pathlib import Path
from collections import defaultdict
import argparse
from tqdm import tqdm
import pickle

try:
    import umap
    import hdbscan
    from sklearn.preprocessing import StandardScaler
    CLUSTERING_AVAILABLE = True
except ImportError:
    CLUSTERING_AVAILABLE = False
    print("⚠️  Install clustering libraries: pip install umap-learn hdbscan scikit-learn")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    print("⚠️  Install plotting libraries: pip install matplotlib seaborn")


class VideoClusterer:
    def __init__(self, channels_dir="channels", cache_dir="video_embeddings_cache"):
        self.channels_dir = Path(channels_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Load CLIP model
        print("🔧 Loading CLIP model...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        print(f"✅ CLIP model loaded on {self.device}")
        
        self.video_files = []
        self.embeddings = None
        self.cluster_labels = None
        
    def find_all_videos(self):
        """Find all video files in channels directory."""
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        self.video_files = []
        
        print(f"🔍 Scanning {self.channels_dir} for videos...")
        for channel_dir in self.channels_dir.iterdir():
            if channel_dir.is_dir() and not channel_dir.name.startswith('.'):
                for video_file in channel_dir.iterdir():
                    if video_file.suffix.lower() in video_extensions:
                        self.video_files.append({
                            'path': video_file,
                            'name': video_file.name,
                            'channel': channel_dir.name,
                            'size_mb': video_file.stat().st_size / (1024 * 1024)
                        })
        
        print(f"✅ Found {len(self.video_files)} videos across {len(set(v['channel'] for v in self.video_files))} channels")
        return self.video_files
    
    def extract_frames(self, video_path, num_frames=5):
        """Extract evenly-spaced frames from video."""
        try:
            cap = cv2.VideoCapture(str(video_path))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if total_frames == 0:
                cap.release()
                return []
            
            # Get evenly spaced frame indices
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            frames = []
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
            
            cap.release()
            return frames
            
        except Exception as e:
            print(f"❌ Error extracting frames from {video_path.name}: {e}")
            return []
    
    def compute_video_embedding(self, video_path, num_frames=5):
        """Compute CLIP embedding for a video by averaging frame embeddings."""
        frames = self.extract_frames(video_path, num_frames)
        
        if not frames:
            return None
        
        embeddings = []
        with torch.no_grad():
            for frame in frames:
                # Preprocess and encode
                from PIL import Image
                pil_image = Image.fromarray(frame)
                image_input = self.preprocess(pil_image).unsqueeze(0).to(self.device)
                embedding = self.model.encode_image(image_input)
                embeddings.append(embedding.cpu().numpy())
        
        # Average embeddings across frames
        avg_embedding = np.mean(embeddings, axis=0)
        # Normalize
        avg_embedding = avg_embedding / np.linalg.norm(avg_embedding)
        
        return avg_embedding.flatten()
    
    def compute_all_embeddings(self, force_recompute=False):
        """Compute embeddings for all videos with caching."""
        cache_file = self.cache_dir / "video_embeddings.pkl"
        
        # Try to load from cache
        if cache_file.exists() and not force_recompute:
            print("📦 Loading embeddings from cache...")
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
                self.video_files = cached_data['video_files']
                self.embeddings = cached_data['embeddings']
                print(f"✅ Loaded {len(self.video_files)} cached embeddings")
                return self.embeddings
        
        # Compute embeddings
        if not self.video_files:
            self.find_all_videos()
        
        print(f"🎬 Computing CLIP embeddings for {len(self.video_files)} videos...")
        print("⏱️  This may take 5-10 minutes...")
        
        embeddings = []
        valid_videos = []
        
        for video_info in tqdm(self.video_files, desc="Processing videos"):
            embedding = self.compute_video_embedding(video_info['path'])
            if embedding is not None:
                embeddings.append(embedding)
                valid_videos.append(video_info)
        
        self.embeddings = np.array(embeddings)
        self.video_files = valid_videos
        
        # Cache results
        print("💾 Caching embeddings...")
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'video_files': self.video_files,
                'embeddings': self.embeddings
            }, f)
        
        print(f"✅ Computed embeddings for {len(self.embeddings)} videos (shape: {self.embeddings.shape})")
        return self.embeddings
    
    def cluster_videos(self, n_neighbors=15, min_cluster_size=10, min_samples=1, assign_all=True):
        """Cluster videos using UMAP + HDBSCAN."""
        if not CLUSTERING_AVAILABLE:
            print("❌ Clustering libraries not available. Install: pip install umap-learn hdbscan scikit-learn")
            return None
        
        if self.embeddings is None:
            print("❌ No embeddings available. Run compute_all_embeddings() first.")
            return None
        
        print("\n🔮 Clustering videos...")
        print(f"📊 Input: {self.embeddings.shape[0]} videos with {self.embeddings.shape[1]}-dim embeddings")
        
        # Step 1: Dimensionality reduction with UMAP
        print(f"   🔸 UMAP: Reducing {self.embeddings.shape[1]} → 5 dimensions...")
        reducer = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            random_state=42,
            verbose=False
        )
        reduced_embeddings = reducer.fit_transform(self.embeddings)
        print(f"   ✅ UMAP complete: {reduced_embeddings.shape}")
        
        # Step 2: Clustering with HDBSCAN
        print(f"   🔸 HDBSCAN: Finding clusters (min_cluster_size={min_cluster_size}, min_samples={min_samples})...")
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric='euclidean',
            cluster_selection_method='eom',
            prediction_data=True  # Enable prediction for outliers
        )
        self.cluster_labels = clusterer.fit_predict(reduced_embeddings)
        
        # Step 2b: Assign outliers to nearest cluster if requested
        if assign_all:
            noise_mask = self.cluster_labels == -1
            num_noise = np.sum(noise_mask)
            if num_noise > 0:
                print(f"   🔸 Assigning {num_noise} outliers to nearest clusters...")
                # Use approximate_predict to assign outliers
                noise_predictions, _ = hdbscan.approximate_predict(clusterer, reduced_embeddings[noise_mask])
                self.cluster_labels[noise_mask] = noise_predictions
                
                # If any still remain as -1, assign to nearest cluster by distance
                still_noise = self.cluster_labels == -1
                if np.sum(still_noise) > 0:
                    from sklearn.metrics.pairwise import euclidean_distances
                    noise_indices = np.where(still_noise)[0]
                    assigned_indices = np.where(~still_noise)[0]
                    
                    for idx in noise_indices:
                        distances = euclidean_distances(
                            reduced_embeddings[idx].reshape(1, -1),
                            reduced_embeddings[assigned_indices]
                        )
                        nearest = assigned_indices[np.argmin(distances)]
                        self.cluster_labels[idx] = self.cluster_labels[nearest]
        
        # Step 3: Also create 2D projection for visualization
        print("   🔸 Creating 2D visualization projection...")
        reducer_2d = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=2,
            min_dist=0.0,
            metric='cosine',
            random_state=42,
            verbose=False
        )
        self.embeddings_2d = reducer_2d.fit_transform(self.embeddings)
        
        # Analyze clusters
        unique_clusters = np.unique(self.cluster_labels)
        num_clusters = len(unique_clusters[unique_clusters >= 0])  # Exclude -1 (noise)
        num_noise = np.sum(self.cluster_labels == -1)
        
        print(f"\n✅ Clustering complete!")
        print(f"   📊 Found {num_clusters} clusters")
        print(f"   🔇 {num_noise} videos marked as noise/outliers")
        
        # Show cluster sizes
        print("\n📈 Cluster sizes:")
        for cluster_id in sorted(unique_clusters):
            count = np.sum(self.cluster_labels == cluster_id)
            if cluster_id == -1:
                print(f"   Noise: {count} videos")
            else:
                print(f"   Cluster {cluster_id}: {count} videos")
        
        return self.cluster_labels
    
    def visualize_clusters(self, save_path="video_clusters_visualization.png"):
        """Create 2D visualization of video clusters."""
        if not PLOTTING_AVAILABLE:
            print("❌ Plotting libraries not available. Install: pip install matplotlib seaborn")
            return
        
        if self.embeddings_2d is None or self.cluster_labels is None:
            print("❌ No clustering results to visualize. Run cluster_videos() first.")
            return
        
        print(f"📊 Creating visualization...")
        
        plt.figure(figsize=(14, 10))
        
        # Create color palette
        unique_clusters = np.unique(self.cluster_labels)
        num_clusters = len(unique_clusters[unique_clusters >= 0])
        colors = sns.color_palette("husl", num_clusters)
        
        # Plot each cluster
        color_idx = 0
        for cluster_id in sorted(unique_clusters):
            mask = self.cluster_labels == cluster_id
            
            if cluster_id == -1:
                # Noise points in gray
                plt.scatter(
                    self.embeddings_2d[mask, 0],
                    self.embeddings_2d[mask, 1],
                    c='lightgray',
                    s=20,
                    alpha=0.3,
                    label=f'Noise ({np.sum(mask)})'
                )
            else:
                # Cluster points
                plt.scatter(
                    self.embeddings_2d[mask, 0],
                    self.embeddings_2d[mask, 1],
                    c=[colors[color_idx]],
                    s=50,
                    alpha=0.7,
                    label=f'Cluster {cluster_id} ({np.sum(mask)})'
                )
                color_idx += 1
        
        plt.title('Video Clustering Visualization (CLIP + UMAP + HDBSCAN)', fontsize=16, fontweight='bold')
        plt.xlabel('UMAP Dimension 1', fontsize=12)
        plt.ylabel('UMAP Dimension 2', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.tight_layout()
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Visualization saved to: {save_path}")
        
        # Also show in window if possible
        try:
            plt.show()
        except:
            pass
    
    def get_cluster_samples(self, cluster_id, num_samples=5):
        """Get sample videos from a cluster."""
        mask = self.cluster_labels == cluster_id
        indices = np.where(mask)[0]
        
        if len(indices) == 0:
            return []
        
        # Get random samples
        sample_indices = np.random.choice(indices, min(num_samples, len(indices)), replace=False)
        samples = [self.video_files[i] for i in sample_indices]
        
        return samples
    
    def export_cluster_report(self, output_file="cluster_analysis.json"):
        """Export detailed cluster analysis."""
        if self.cluster_labels is None:
            print("❌ No clustering results. Run cluster_videos() first.")
            return
        
        report = {
            'summary': {
                'total_videos': len(self.video_files),
                'num_clusters': len(np.unique(self.cluster_labels[self.cluster_labels >= 0])),
                'num_noise': int(np.sum(self.cluster_labels == -1))
            },
            'clusters': {}
        }
        
        # Analyze each cluster
        for cluster_id in sorted(np.unique(self.cluster_labels)):
            mask = self.cluster_labels == cluster_id
            cluster_videos = [self.video_files[i] for i in np.where(mask)[0]]
            
            # Get channel distribution
            channel_counts = defaultdict(int)
            for video in cluster_videos:
                channel_counts[video['channel']] += 1
            
            cluster_name = "noise" if cluster_id == -1 else f"cluster_{cluster_id}"
            
            report['clusters'][cluster_name] = {
                'id': int(cluster_id),
                'size': len(cluster_videos),
                'channel_distribution': dict(channel_counts),
                'sample_videos': [v['name'] for v in cluster_videos]  # Save ALL videos, not just samples
            }
        
        # Save report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Cluster report saved to: {output_file}")
        return report
    
    def preview_reorganization(self):
        """Preview how videos would be reorganized into new channels."""
        if self.cluster_labels is None:
            print("❌ No clustering results. Run cluster_videos() first.")
            return
        
        print("\n" + "="*80)
        print("📋 REORGANIZATION PREVIEW")
        print("="*80)
        
        for cluster_id in sorted(np.unique(self.cluster_labels)):
            if cluster_id == -1:
                continue  # Skip noise for now
            
            mask = self.cluster_labels == cluster_id
            cluster_videos = [self.video_files[i] for i in np.where(mask)[0]]
            
            # Show cluster info
            print(f"\n🎯 New Channel: Cluster_{cluster_id:02d} ({len(cluster_videos)} videos)")
            
            # Show original channel distribution
            channel_counts = defaultdict(int)
            for video in cluster_videos:
                channel_counts[video['channel']] += 1
            
            print(f"   📊 Source channels:")
            for channel, count in sorted(channel_counts.items(), key=lambda x: -x[1])[:5]:
                print(f"      • {channel}: {count} videos")
            
            # Show sample videos
            print(f"   📝 Sample videos:")
            for video in cluster_videos[:3]:
                print(f"      • {video['name'][:60]}...")


def main():
    parser = argparse.ArgumentParser(description="Advanced Video Clustering with CLIP")
    parser.add_argument("command", choices=['analyze', 'visualize', 'report', 'preview', 'full'],
                       help="Command to run")
    parser.add_argument("--channels-dir", default="channels", help="Directory containing video channels")
    parser.add_argument("--force", action="store_true", help="Force recompute embeddings")
    parser.add_argument("--min-cluster-size", type=int, default=10, 
                       help="Minimum cluster size (default: 10)")
    parser.add_argument("--neighbors", type=int, default=15,
                       help="UMAP n_neighbors parameter (default: 15)")
    
    args = parser.parse_args()
    
    # Create clusterer
    clusterer = VideoClusterer(channels_dir=args.channels_dir)
    
    if args.command in ['analyze', 'full']:
        # Step 1: Find videos and compute embeddings
        clusterer.find_all_videos()
        clusterer.compute_all_embeddings(force_recompute=args.force)
        
        # Step 2: Cluster videos
        clusterer.cluster_videos(
            n_neighbors=args.neighbors,
            min_cluster_size=args.min_cluster_size
        )
    
    if args.command in ['visualize', 'full']:
        # Create visualization
        if clusterer.cluster_labels is None:
            print("⚠️  Loading cached results...")
            clusterer.compute_all_embeddings()
            clusterer.cluster_videos()
        
        clusterer.visualize_clusters()
    
    if args.command in ['report', 'full']:
        # Export report
        if clusterer.cluster_labels is None:
            print("⚠️  Loading cached results...")
            clusterer.compute_all_embeddings()
            clusterer.cluster_videos()
        
        clusterer.export_cluster_report()
    
    if args.command in ['preview', 'full']:
        # Preview reorganization
        if clusterer.cluster_labels is None:
            print("⚠️  Loading cached results...")
            clusterer.compute_all_embeddings()
            clusterer.cluster_videos()
        
        clusterer.preview_reorganization()
    
    print("\n✅ Done!")
    print("\n💡 Next steps:")
    print("   • Review cluster_analysis.json for detailed breakdown")
    print("   • Check video_clusters_visualization.png to see groupings")
    print("   • Adjust --min-cluster-size to get more/fewer clusters")


if __name__ == "__main__":
    main()
