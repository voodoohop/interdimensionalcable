#!/usr/bin/env python3
"""
Semantic Video Analyzer - Split videos into themed channels based on content analysis.
Uses visual statistics + simple CLIP categorization for robust results.
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
import shutil
import argparse

def analyze_visual_stats(image_path):
    """
    Analyze basic visual statistics of an image.
    Returns: dict with brightness, contrast, saturation, dominant_colors
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    # Convert to different color spaces
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate statistics
    brightness = np.mean(gray)
    contrast = np.std(gray)
    saturation = np.mean(hsv[:,:,1])
    
    # Dominant colors (simplified)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3)
    
    # Simple color categorization
    avg_color = np.mean(pixels, axis=0)
    
    # Determine color category
    r, g, b = avg_color
    if max(r, g, b) - min(r, g, b) < 30:  # Low color variation
        if brightness < 80:
            color_category = "dark_monochrome"
        elif brightness > 180:
            color_category = "bright_monochrome"
        else:
            color_category = "neutral_monochrome"
    else:  # Colorful
        if r > g and r > b:
            color_category = "warm_colors"
        elif b > r and b > g:
            color_category = "cool_colors"
        elif g > r and g > b:
            color_category = "natural_colors"
        else:
            color_category = "mixed_colors"
    
    return {
        'brightness': float(brightness),
        'contrast': float(contrast),
        'saturation': float(saturation),
        'color_category': color_category,
        'avg_color': [float(r), float(g), float(b)]
    }

def analyze_video_content(screenshots_folder):
    """
    Analyze all screenshots for a video and return aggregated stats.
    """
    screenshots = list(Path(screenshots_folder).glob("*.jpg"))
    if not screenshots:
        return None
    
    all_stats = []
    for screenshot in screenshots:
        stats = analyze_visual_stats(screenshot)
        if stats:
            all_stats.append(stats)
    
    if not all_stats:
        return None
    
    # Aggregate statistics
    avg_brightness = np.mean([s['brightness'] for s in all_stats])
    avg_contrast = np.mean([s['contrast'] for s in all_stats])
    avg_saturation = np.mean([s['saturation'] for s in all_stats])
    
    # Most common color category
    color_categories = [s['color_category'] for s in all_stats]
    dominant_color_category = Counter(color_categories).most_common(1)[0][0]
    
    # Determine visual style
    if avg_brightness < 60:
        style = "dark"
    elif avg_brightness > 180:
        style = "bright"
    elif avg_saturation < 50:
        style = "monochrome"
    elif avg_saturation > 150:
        style = "vibrant"
    else:
        style = "balanced"
    
    return {
        'brightness': avg_brightness,
        'contrast': avg_contrast,
        'saturation': avg_saturation,
        'color_category': dominant_color_category,
        'visual_style': style,
        'screenshot_count': len(all_stats)
    }

def simple_content_categorization(screenshots_folder):
    """
    Simple content categorization based on visual patterns.
    This is a placeholder for CLIP analysis - we'll use visual heuristics for now.
    """
    screenshots = list(Path(screenshots_folder).glob("*.jpg"))
    if not screenshots:
        return "unknown"
    
    # Analyze first screenshot for content hints
    img = cv2.imread(str(screenshots[0]))
    if img is None:
        return "unknown"
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple heuristics based on edge detection and texture
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    
    # Texture analysis
    texture = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Simple categorization based on visual features
    if edge_density > 0.1 and texture > 500:
        return "complex_detailed"  # Likely urban, technology, or detailed scenes
    elif edge_density < 0.05 and texture < 100:
        return "simple_abstract"   # Likely abstract, minimal, or simple scenes
    elif texture > 300:
        return "natural_organic"   # Likely nature, organic textures
    else:
        return "balanced_content"  # Mixed content

def categorize_videos(screenshots_base_dir):
    """
    Categorize all videos based on their screenshots.
    """
    screenshots_base = Path(screenshots_base_dir)
    
    # Find all video screenshot folders
    video_folders = {}
    
    # Look for screenshot folders
    for channel_folder in screenshots_base.iterdir():
        if channel_folder.is_dir():
            print(f"📁 Analyzing channel: {channel_folder.name}")
            
            # Group screenshots by video name
            video_screenshots = defaultdict(list)
            
            for screenshot in channel_folder.glob("*.jpg"):
                # Extract video name from screenshot filename
                # Format: videoname_frame_XX_Xs.jpg
                parts = screenshot.stem.split('_frame_')
                if len(parts) >= 2:
                    video_name = parts[0]
                    video_screenshots[video_name].append(screenshot)
            
            # Analyze each video
            for video_name, screenshots in video_screenshots.items():
                print(f"  🎬 Analyzing: {video_name}")
                
                # Create temporary folder for this video's screenshots
                temp_folder = screenshots_base / "temp" / video_name
                temp_folder.mkdir(parents=True, exist_ok=True)
                
                # Copy screenshots to temp folder
                for screenshot in screenshots:
                    shutil.copy2(screenshot, temp_folder)
                
                # Analyze video
                visual_stats = analyze_video_content(temp_folder)
                content_category = simple_content_categorization(temp_folder)
                
                if visual_stats:
                    video_folders[video_name] = {
                        'original_channel': channel_folder.name,
                        'visual_stats': visual_stats,
                        'content_category': content_category,
                        'screenshots': [str(s) for s in screenshots]
                    }
                
                # Clean up temp folder
                shutil.rmtree(temp_folder)
    
    # Clean up temp directory
    temp_dir = screenshots_base / "temp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    return video_folders

def create_semantic_channels(video_analysis, output_dir="semantic_channels"):
    """
    Create new channel folders based on semantic analysis.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Define channel categories based on analysis
    channels = {
        'dark_atmospheric': {
            'name': 'Dark Atmospheric',
            'criteria': lambda v: v['visual_stats']['visual_style'] == 'dark',
            'videos': []
        },
        'bright_energetic': {
            'name': 'Bright Energetic', 
            'criteria': lambda v: v['visual_stats']['visual_style'] == 'bright',
            'videos': []
        },
        'vibrant_colorful': {
            'name': 'Vibrant Colorful',
            'criteria': lambda v: v['visual_stats']['visual_style'] == 'vibrant',
            'videos': []
        },
        'monochrome_minimal': {
            'name': 'Monochrome Minimal',
            'criteria': lambda v: v['visual_stats']['visual_style'] == 'monochrome',
            'videos': []
        },
        'complex_detailed': {
            'name': 'Complex Detailed',
            'criteria': lambda v: v['content_category'] == 'complex_detailed',
            'videos': []
        },
        'abstract_artistic': {
            'name': 'Abstract Artistic',
            'criteria': lambda v: v['content_category'] == 'simple_abstract',
            'videos': []
        },
        'natural_organic': {
            'name': 'Natural Organic',
            'criteria': lambda v: v['content_category'] == 'natural_organic',
            'videos': []
        },
        'balanced_mixed': {
            'name': 'Balanced Mixed',
            'criteria': lambda v: True,  # Catch-all
            'videos': []
        }
    }
    
    # Categorize videos
    for video_name, analysis in video_analysis.items():
        assigned = False
        
        # Try to assign to specific categories first
        for channel_id, channel_info in list(channels.items())[:-1]:  # Skip catch-all
            if channel_info['criteria'](analysis):
                channel_info['videos'].append(video_name)
                assigned = True
                break
        
        # If not assigned, put in catch-all
        if not assigned:
            channels['balanced_mixed']['videos'].append(video_name)
    
    # Create channel folders and copy videos
    original_videos_dir = Path("channels/02_Random_Veo3_Videos")
    
    channel_summary = {}
    
    for channel_id, channel_info in channels.items():
        if not channel_info['videos']:
            continue
            
        # Create channel folder
        channel_folder = output_path / f"{len(channel_summary)+1:02d}_{channel_id}"
        channel_folder.mkdir(exist_ok=True)
        
        # Copy videos
        copied_count = 0
        for video_name in channel_info['videos']:
            # Find the actual video file
            video_files = list(original_videos_dir.glob(f"{video_name}.*"))
            for video_file in video_files:
                if video_file.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                    dest_path = channel_folder / video_file.name
                    if not dest_path.exists():
                        shutil.copy2(video_file, dest_path)
                        copied_count += 1
        
        if copied_count > 0:
            channel_summary[channel_id] = {
                'name': channel_info['name'],
                'folder': str(channel_folder),
                'video_count': copied_count,
                'videos': channel_info['videos'][:5]  # Sample of videos
            }
    
    return channel_summary

def main():
    parser = argparse.ArgumentParser(description="Semantic video analysis and channel creation")
    parser.add_argument("--screenshots-dir", default="screenshots", 
                       help="Directory containing video screenshots")
    parser.add_argument("--output-dir", default="semantic_channels",
                       help="Output directory for semantic channels")
    parser.add_argument("--dry-run", action="store_true",
                       help="Analyze only, don't create channels")
    
    args = parser.parse_args()
    
    print("🎬 Starting semantic video analysis...")
    print("=" * 60)
    
    # Analyze videos
    print("📊 Analyzing video content...")
    video_analysis = categorize_videos(args.screenshots_dir)
    
    print(f"\n✅ Analyzed {len(video_analysis)} videos")
    
    # Show analysis summary
    styles = defaultdict(int)
    categories = defaultdict(int)
    
    for video_name, analysis in video_analysis.items():
        styles[analysis['visual_stats']['visual_style']] += 1
        categories[analysis['content_category']] += 1
    
    print("\n📈 Visual Styles:")
    for style, count in sorted(styles.items()):
        print(f"  {style}: {count} videos")
    
    print("\n📈 Content Categories:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} videos")
    
    if not args.dry_run:
        print(f"\n🎯 Creating semantic channels in '{args.output_dir}'...")
        channel_summary = create_semantic_channels(video_analysis, args.output_dir)
        
        print("\n✅ Created channels:")
        for channel_id, info in channel_summary.items():
            print(f"  📁 {info['name']}: {info['video_count']} videos")
            print(f"     Sample videos: {', '.join(info['videos'][:3])}...")
        
        # Save analysis results
        results_file = Path(args.output_dir) / "analysis_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'video_analysis': video_analysis,
                'channel_summary': channel_summary
            }, f, indent=2)
        
        print(f"\n💾 Analysis results saved to: {results_file}")
        print(f"🎉 Semantic channel creation complete!")
    else:
        print("\n🔍 Dry run complete - no channels created")

if __name__ == "__main__":
    main()
