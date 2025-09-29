#!/usr/bin/env python3
"""Create a test config with already uploaded videos"""

import json
from pathlib import Path

# Load progress
with open('stream_upload_progress.json', 'r') as f:
    data = json.load(f)

# Get successful uploads
successful = [r for r in data['results'] if r.get('success')]
print(f'Found {len(successful)} successfully uploaded videos')

# Create filename to URL mapping
filename_to_url = {r['filename']: r['iframe_url'] for r in successful}

# Load original channels
with open('channels_clustered.json', 'r') as f:
    data = json.load(f)
    channels = data['channels'] if 'channels' in data else data

# Create test config with uploaded videos
test_channels = []
used_count = 0

for channel in channels:
    test_channel = {
        'name': channel['name'],
        'folder': channel['folder'],
        'videos': []
    }
    
    # Match videos by filename
    for video_file in channel['videos']:
        # Handle both string filenames and dict objects
        if isinstance(video_file, str):
            filename = video_file
        else:
            filename = video_file.get('url', '').split('/')[-1]
        
        if filename in filename_to_url:
            test_channel['videos'].append({
                'url': filename_to_url[filename],
                'title': filename
            })
            used_count += 1
    
    # Only include channels with uploaded videos
    if test_channel['videos']:
        test_channels.append(test_channel)

print(f'Created test config with {len(test_channels)} channels and {used_count} videos')

# Save test config
with open('channels_clustered_stream_test.json', 'w') as f:
    json.dump(test_channels, f, indent=2)

print('✅ Saved to: channels_clustered_stream_test.json')
print('\nTo test:')
print('1. Edit tv_clustered_stream.html line ~238')
print('   Change: fetch(\'channels_clustered_stream.json\')')
print('   To:     fetch(\'channels_clustered_stream_test.json\')')
print('2. Open tv_clustered_stream.html in browser')
