#!/bin/bash
# Setup script for video clustering system

echo "🔧 Setting up video clustering dependencies..."
echo ""

# Install CLIP
echo "📦 Installing CLIP..."
pip install torch torchvision
pip install git+https://github.com/openai/CLIP.git

# Install clustering libraries
echo "📦 Installing clustering libraries..."
pip install umap-learn hdbscan scikit-learn

# Install visualization
echo "📦 Installing visualization libraries..."
pip install matplotlib seaborn

# Install video processing
echo "📦 Installing OpenCV and Pillow..."
pip install opencv-python pillow

# Install progress bar
echo "📦 Installing tqdm..."
pip install tqdm

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Run the clusterer with:"
echo "   python3 advanced_video_clusterer.py full"
echo ""
