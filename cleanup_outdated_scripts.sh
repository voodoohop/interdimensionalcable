#!/bin/bash
# Cleanup outdated and broken scripts

echo "🧹 Cleaning up outdated scripts..."

# Outdated clustering scripts (replaced by recluster_and_update_json.py)
rm -f scripts/clustering/prepare_combined_clustering.py
rm -f scripts/clustering/apply_clustering_results.py

# Outdated utility scripts (replaced by add_new_videos_to_channels.py)
rm -f scripts/utilities/update_channels.py
rm -f scripts/utilities/update_clustered_channels.py

# Outdated upload script (replaced by upload_new_videos.py)
# Keep upload_to_stream.py as it may still be useful for batch operations

# Outdated export script (embeddings are now in pickle format)
rm -f scripts/export_embeddings_to_json.py

echo "✅ Cleanup complete!"
echo ""
echo "Removed scripts:"
echo "  - scripts/clustering/prepare_combined_clustering.py"
echo "  - scripts/clustering/apply_clustering_results.py"
echo "  - scripts/utilities/update_channels.py"
echo "  - scripts/utilities/update_clustered_channels.py"
echo "  - scripts/export_embeddings_to_json.py"
echo ""
echo "Active scripts:"
echo "  📦 import_and_deploy_videos.py (MASTER PIPELINE)"
echo "  📁 scripts/utilities/import_new_videos.py"
echo "  📤 scripts/stream_upload/upload_new_videos.py"
echo "  📺 scripts/utilities/add_new_videos_to_channels.py"
echo "  🔀 scripts/clustering/recluster_and_update_json.py"
echo "  🧠 scripts/clustering/advanced_video_clusterer.py"
