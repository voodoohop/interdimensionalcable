#!/bin/bash
# Check clustering progress

echo "🔍 Checking clustering progress..."
echo ""

# Check if process is running
if ps aux | grep "advanced_video_clusterer" | grep -v grep > /dev/null; then
    echo "✅ Clustering process is running"
    echo ""
fi

# Check for cache files
if [ -d "video_embeddings_cache" ]; then
    echo "📦 Cache directory exists:"
    ls -lh video_embeddings_cache/
    echo ""
fi

# Check for output files
if [ -f "video_clusters_visualization.png" ]; then
    echo "📊 Visualization created:"
    ls -lh video_clusters_visualization.png
    echo ""
fi

if [ -f "cluster_analysis.json" ]; then
    echo "📄 Analysis report created:"
    ls -lh cluster_analysis.json
    head -20 cluster_analysis.json
    echo ""
fi

echo "💡 To monitor in real-time, run:"
echo "   tail -f clustering.log"
