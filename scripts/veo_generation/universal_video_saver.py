#!/usr/bin/env python3
"""
Universal Video Saver - Monitors all operation files and downloads completed videos
"""

import json
import glob
import base64
import subprocess
import requests
import os
from datetime import datetime

def get_access_token():
    """Get Google Cloud access token"""
    result = subprocess.run(['/opt/homebrew/bin/gcloud', 'auth', 'print-access-token'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to get access token: {result.stderr}")
    return result.stdout.strip()

def fetch_operation_result(operation_name):
    """Fetch operation result using fetchPredictOperation endpoint"""
    access_token = get_access_token()
    
    # Extract model info from operation name
    parts = operation_name.split('/')
    project_id = parts[1]
    location = parts[3]
    model_id = parts[7]
    
    endpoint = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{model_id}:fetchPredictOperation"
    
    payload = {"operationName": operation_name}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def save_base64_video(base64_data, title, operation_name, init_image=None, category="unknown"):
    """Save base64 video data to file"""
    try:
        # Decode base64 data
        video_bytes = base64.b64decode(base64_data)
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.replace(" ", "_").replace("-", "_").replace(":", "").replace("/", "_")
        filename = f"{timestamp}_{safe_title}.mp4"
        filepath = f"generated_videos/{filename}"
        
        # Ensure directory exists
        os.makedirs("generated_videos", exist_ok=True)
        
        # Save video
        with open(filepath, 'wb') as f:
            f.write(video_bytes)
        
        # Save metadata
        metadata = {
            "title": title,
            "local_path": filepath,
            "downloaded_at": datetime.now().isoformat(),
            "operation_name": operation_name,
            "init_image": init_image,
            "category": category,
            "video_index": 0,
            "mime_type": "video/mp4",
            "file_size_mb": round(len(video_bytes) / (1024 * 1024), 1)
        }
        
        metadata_path = filepath.replace('.mp4', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ SAVED: {title}")
        print(f"   📁 File: {filepath}")
        print(f"   💾 Size: {metadata['file_size_mb']} MB")
        print(f"   🎨 Category: {category}")
        if init_image:
            print(f"   🖼️  Init: {init_image}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save video: {e}")
        return False

def main():
    """Main function to check all operation files"""
    
    print("🎬 UNIVERSAL VIDEO SAVER")
    print("=" * 60)
    
    # Find all operation files
    operation_files = glob.glob("*operations*.json")
    
    if not operation_files:
        print("❌ No operation files found")
        return
    
    print(f"📁 Found {len(operation_files)} operation files")
    
    saved_count = 0
    total_operations = 0
    
    for file_path in sorted(operation_files):
        print(f"\n📄 Processing: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                operations = json.load(f)
            
            if not operations:
                continue
                
            for op in operations:
                total_operations += 1
                
                # Handle different operation file formats
                operation_name = op.get('operation_name') or op.get('name')
                title = op.get('title', 'Unknown Title')
                init_image = op.get('init_image')
                category = op.get('category', 'unknown')
                
                if not operation_name:
                    print(f"   ⚠️  {title} - No operation name")
                    continue
                
                print(f"   🔍 Checking: {title}")
                
                result = fetch_operation_result(operation_name)
                
                if result and result.get('done'):
                    if result.get('error'):
                        error_code = result['error'].get('code')
                        if error_code == 3:
                            print(f"   🚫 BLOCKED: Safety filter")
                        else:
                            print(f"   ❌ ERROR: {result['error'].get('message', 'Unknown error')}")
                    elif 'response' in result and 'videos' in result['response']:
                        videos = result['response']['videos']
                        for i, video_data in enumerate(videos):
                            if 'bytesBase64Encoded' in video_data:
                                success = save_base64_video(
                                    video_data['bytesBase64Encoded'],
                                    title,
                                    operation_name,
                                    init_image,
                                    category
                                )
                                if success:
                                    saved_count += 1
                            else:
                                print(f"   ⚠️  No base64 data found")
                    else:
                        print(f"   ⚠️  No videos in response")
                elif result and not result.get('done'):
                    print(f"   ⏳ Still generating...")
                else:
                    print(f"   ❓ Operation not found")
                    
        except Exception as e:
            print(f"   ❌ Error processing file: {e}")
    
    print(f"\n📊 UNIVERSAL DOWNLOAD SUMMARY:")
    print(f"🎬 Total operations checked: {total_operations}")
    print(f"✅ Videos downloaded this session: {saved_count}")
    print(f"📁 Save location: generated_videos/")
    
    # Count total videos
    video_files = glob.glob("generated_videos/*.mp4")
    total_size = sum(os.path.getsize(f) for f in video_files) / (1024 * 1024)
    
    print(f"📁 Total videos in collection: {len(video_files)}")
    print(f"💾 Total collection size: {total_size:.1f} MB")
    
    if saved_count > 0:
        print(f"\n🎉 SUCCESS! Downloaded {saved_count} new videos!")
    else:
        print(f"\n😞 No new videos downloaded this time.")

if __name__ == "__main__":
    main()
