#!/usr/bin/env python3
"""
Master pipeline for importing new videos to Interdimensional Cable.

This script handles the complete workflow:
1. Import videos from a source directory
2. Upload to Cloudflare Stream
3. Either add as new channel OR semantically recluster all videos
4. Update configuration and prepare for deployment

Usage:
    # Simple workflow (add as new channel):
    python3 import_and_deploy_videos.py <source_directory> --prefix <prefix>
    
    # With semantic reclustering:
    python3 import_and_deploy_videos.py <source_directory> --prefix <prefix> --recluster
    
Examples:
    python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels
    python3 import_and_deploy_videos.py ~/Downloads/new_videos --prefix ale --recluster
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        sys.exit(1)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(
        description='Import and deploy videos to Interdimensional Cable',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add videos as a new channel (fast):
  python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels
  
  # Add and semantically recluster all videos (slower but better organization):
  python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels --recluster
  
  # Dry run (don't deploy):
  python3 import_and_deploy_videos.py generated_videos/vkdels --prefix vkdels --no-deploy
        """
    )
    
    parser.add_argument('source_directory', help='Directory containing videos to import')
    parser.add_argument('--prefix', default='video', help='Prefix for imported videos (default: video)')
    parser.add_argument('--staging-dir', default='new_videos_staging', 
                       help='Staging directory (default: new_videos_staging)')
    parser.add_argument('--recluster', action='store_true',
                       help='Semantically recluster all videos (slower but better organization)')
    parser.add_argument('--min-cluster-size', type=int, default=7,
                       help='Minimum cluster size for reclustering (default: 7)')
    parser.add_argument('--no-deploy', action='store_true',
                       help='Skip git commit and push')
    parser.add_argument('--clean-staging', action='store_true',
                       help='Clean staging directory before import')
    
    args = parser.parse_args()
    
    # Validate source directory
    source_path = Path(args.source_directory)
    if not source_path.exists():
        print(f"❌ Source directory not found: {args.source_directory}")
        sys.exit(1)
    
    # Clean staging directory if requested
    if args.clean_staging:
        staging_path = Path(args.staging_dir)
        if staging_path.exists():
            print(f"🧹 Cleaning staging directory: {args.staging_dir}")
            import shutil
            shutil.rmtree(staging_path)
    
    print("="*60)
    print("🎬 INTERDIMENSIONAL CABLE - VIDEO IMPORT PIPELINE")
    print("="*60)
    print(f"📁 Source: {args.source_directory}")
    print(f"🏷️  Prefix: {args.prefix}")
    print(f"📂 Staging: {args.staging_dir}")
    print(f"🔀 Recluster: {'Yes' if args.recluster else 'No'}")
    print(f"🚀 Deploy: {'No (dry run)' if args.no_deploy else 'Yes'}")
    print("="*60)
    
    # Step 1: Import videos
    run_command(
        f"python3 scripts/utilities/import_new_videos.py {args.source_directory} {args.staging_dir} {args.prefix}",
        "Step 1/4: Importing videos with proper naming"
    )
    
    # Step 2: Upload to Cloudflare Stream
    run_command(
        f"python3 scripts/stream_upload/upload_new_videos.py {args.staging_dir}",
        "Step 2/4: Uploading to Cloudflare Stream"
    )
    
    # Step 3: Update channels (either simple or with reclustering)
    if args.recluster:
        run_command(
            f"python3 scripts/clustering/recluster_and_update_json.py --min-cluster-size {args.min_cluster_size}",
            "Step 3/4: Semantically reclustering all videos"
        )
        commit_message = f"Add videos with semantic reclustering ({args.prefix})"
    else:
        run_command(
            "python3 scripts/utilities/add_new_videos_to_channels.py",
            "Step 3/4: Adding videos to new channel"
        )
        commit_message = f"Add new videos to channel ({args.prefix})"
    
    # Step 4: Deploy
    if not args.no_deploy:
        print(f"\n{'='*60}")
        print("🚀 Step 4/4: Deploying to production")
        print(f"{'='*60}")
        
        run_command(
            "git add channels_clustered_stream.json public/channels_clustered_stream.json",
            "Staging files"
        )
        
        run_command(
            f'git commit -m "{commit_message}"',
            "Committing changes"
        )
        
        run_command(
            "git push origin main",
            "Pushing to GitHub"
        )
        
        print(f"\n{'='*60}")
        print("✅ DEPLOYMENT COMPLETE!")
        print(f"{'='*60}")
        print("🎉 Your videos are now live on Interdimensional Cable!")
    else:
        print(f"\n{'='*60}")
        print("✅ PIPELINE COMPLETE (DRY RUN)")
        print(f"{'='*60}")
        print("📝 Changes staged but not deployed")
        print("\nTo deploy manually:")
        print("  git add channels_clustered_stream.json public/channels_clustered_stream.json")
        print(f'  git commit -m "{commit_message}"')
        print("  git push origin main")
    
    print("\n🎯 Next steps:")
    print("  • Test locally: open html_apps/tv_clustered_stream.html")
    print("  • View live site: https://voodoohop.github.io/interdimensionalcable/")

if __name__ == '__main__':
    main()
