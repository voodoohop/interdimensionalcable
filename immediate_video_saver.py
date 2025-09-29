#!/usr/bin/env python3
"""
Immediate Video Saver - Decodes base64 video data and saves to file
"""

import base64
import json
import subprocess
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
    # Format: projects/PROJECT/locations/LOCATION/publishers/google/models/MODEL/operations/OPERATION_ID
    parts = operation_name.split('/')
    project_id = parts[1]
    location = parts[3]
    # Skip 'publishers', 'google', 'models' and get the actual model name
    model_id = parts[7]  # This should be 'veo-3.0-generate-001'
    
    endpoint = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{model_id}:fetchPredictOperation"
    
    print(f"   🔗 Endpoint: {endpoint}")
    print(f"   📝 Operation: {operation_name}")
    
    payload = {
        "operationName": operation_name
    }
    
    import requests
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to fetch operation: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def save_base64_video(base64_data, title, operation_name, init_image=None):
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
        print(f"   🖼️  Init: {init_image}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save video: {e}")
        return False

def main():
    """Main function to save videos from our recent operations"""
    
    # Load operations from the most recent diverse operations files (with init images)
    operation_files = [
        "diverse_operations_20250929_095911.json",
        "diverse_operations_20250929_095929.json", 
        "diverse_operations_20250929_095954.json"
    ]
    
    # Also check these specific operations
    operations = [
        {
            "name": "projects/pollinations-430910/locations/us-central1/publishers/google/models/veo-3.0-generate-001/operations/582e2d8e-52c4-4a33-bcb3-753e54e8b741",
            "title": "Retro TV screens displaying",
            "init_image": "init_01.jpeg"
        },
        {
            "name": "projects/pollinations-430910/locations/us-central1/publishers/google/models/veo-3.0-generate-001/operations/f4e4a090-8dad-4ace-8e65-444df65904ee",
            "title": "Soap bubble surface tension",
            "init_image": "init_03.jpeg"
        },
        {
            "name": "projects/pollinations-430910/locations/us-central1/publishers/google/models/veo-3.0-generate-001/operations/fd92ac10-c487-45dd-a42b-ca450a03d3a2",
            "title": "Swirling galaxies of paint",
            "init_image": "init_06.jpeg"
        },
        {
            "name": "projects/pollinations-430910/locations/us-central1/publishers/google/models/veo-3.0-generate-001/operations/ed9b5f2b-a8f4-434b-8046-4dd0e13e8da3",
            "title": "Cassette tapes transforming into",
            "init_image": "init_05.jpeg"
        }
    ]
    
    print("🎬 IMMEDIATE VIDEO SAVER")
    print("=" * 60)
    
    saved_count = 0
    
    for op in operations:
        print(f"\n🔍 Checking: {op['title']}")
        
        result = fetch_operation_result(op['name'])
        
        if result and result.get('done'):
            if 'response' in result and 'videos' in result['response']:
                videos = result['response']['videos']
                for i, video_data in enumerate(videos):
                    if 'bytesBase64Encoded' in video_data:
                        success = save_base64_video(
                            video_data['bytesBase64Encoded'],
                            op['title'],
                            op['name'],
                            op['init_image']
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
            print(f"   ❌ Operation not found or failed")
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Videos saved: {saved_count}")
    print(f"📁 Location: generated_videos/")
    
    if saved_count > 0:
        print(f"\n🎉 SUCCESS! Downloaded {saved_count} new videos!")
    else:
        print(f"\n😞 No new videos downloaded this time.")

if __name__ == "__main__":
    main()
