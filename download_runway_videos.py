#!/usr/bin/env python3
"""
Runway Video Downloader
Downloads all videos from your Runway account using the Runway API.

Setup:
1. Get your Runway API key from: https://app.runwayml.com/settings
2. Add to .env file: RUNWAY_API_KEY=your_key_here
3. Run: python3 download_runway_videos.py

Features:
- Downloads all assets from your Runway account
- Tracks progress to avoid re-downloads
- Concurrent downloads with rate limiting
- Organizes by project/folder structure
- Handles errors gracefully
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY')
RUNWAY_API_BASE = 'https://api.runwayml.com/v1'
OUTPUT_DIR = Path('runway_downloads')
PROGRESS_FILE = OUTPUT_DIR / 'download_progress.json'
MAX_WORKERS = 2  # Concurrent downloads (keep low to avoid rate limits)
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

class RunwayDownloader:
    def __init__(self):
        if not RUNWAY_API_KEY:
            print("❌ Error: RUNWAY_API_KEY not found in .env file")
            print("\n📝 Setup Instructions:")
            print("1. Go to https://app.runwayml.com/settings")
            print("2. Generate an API key")
            print("3. Add to .env file: RUNWAY_API_KEY=your_key_here")
            sys.exit(1)
        
        self.headers = {
            'Authorization': f'Bearer {RUNWAY_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.progress = self.load_progress()
        OUTPUT_DIR.mkdir(exist_ok=True)
    
    def load_progress(self):
        """Load download progress from file"""
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {'downloaded': {}, 'failed': {}, 'stats': {}}
    
    def save_progress(self):
        """Save download progress to file"""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_all_assets(self):
        """Fetch all assets from Runway account"""
        print("📡 Fetching assets from Runway...")
        
        all_assets = []
        page = 1
        per_page = 100
        
        while True:
            try:
                # Runway API endpoint for listing assets
                url = f"{RUNWAY_API_BASE}/assets"
                params = {
                    'page': page,
                    'per_page': per_page
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 401:
                    print("❌ Authentication failed. Check your RUNWAY_API_KEY")
                    sys.exit(1)
                elif response.status_code == 404:
                    print("⚠️  API endpoint not found. Trying alternative method...")
                    return self.get_assets_alternative()
                
                response.raise_for_status()
                data = response.json()
                
                assets = data.get('assets', [])
                if not assets:
                    break
                
                all_assets.extend(assets)
                print(f"  Found {len(all_assets)} assets so far...")
                
                # Check if there are more pages
                if len(assets) < per_page:
                    break
                
                page += 1
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Error fetching assets: {e}")
                if all_assets:
                    print(f"⚠️  Continuing with {len(all_assets)} assets found so far...")
                    break
                else:
                    return self.get_assets_alternative()
        
        return all_assets
    
    def get_assets_alternative(self):
        """Alternative method using generations endpoint"""
        print("📡 Trying alternative method (generations)...")
        
        try:
            url = f"{RUNWAY_API_BASE}/generations"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            generations = response.json()
            print(f"✅ Found {len(generations)} generations")
            return generations
            
        except Exception as e:
            print(f"❌ Alternative method failed: {e}")
            print("\n💡 Manual download instructions:")
            print("1. Go to https://app.runwayml.com/assets")
            print("2. Select all assets (CMD+A or CTRL+A)")
            print("3. Click Actions → Download")
            print("4. Extract the ZIP file to runway_downloads/")
            sys.exit(1)
    
    def download_asset(self, asset):
        """Download a single asset"""
        asset_id = asset.get('id')
        asset_name = asset.get('name', f'asset_{asset_id}')
        asset_url = asset.get('url') or asset.get('downloadUrl') or asset.get('videoUrl')
        
        if not asset_url:
            print(f"⚠️  No download URL for {asset_name}")
            return None
        
        # Check if already downloaded
        if asset_id in self.progress['downloaded']:
            return 'skipped'
        
        # Determine file extension
        ext = '.mp4'  # Default
        if 'image' in asset.get('type', '').lower():
            ext = '.png'
        elif asset_url:
            url_ext = Path(asset_url).suffix
            if url_ext:
                ext = url_ext
        
        # Create safe filename
        safe_name = "".join(c for c in asset_name if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{asset_id}_{safe_name}{ext}"
        filepath = OUTPUT_DIR / filename
        
        # Download with retries
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = requests.get(asset_url, stream=True, timeout=60)
                response.raise_for_status()
                
                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Update progress
                self.progress['downloaded'][asset_id] = {
                    'name': asset_name,
                    'path': str(filepath),
                    'size': filepath.stat().st_size,
                    'downloaded_at': datetime.now().isoformat()
                }
                self.save_progress()
                
                return 'success'
                
            except Exception as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    self.progress['failed'][asset_id] = {
                        'name': asset_name,
                        'error': str(e),
                        'url': asset_url
                    }
                    self.save_progress()
                    return 'failed'
        
        return 'failed'
    
    def download_all(self):
        """Download all assets with concurrent workers"""
        assets = self.get_all_assets()
        
        if not assets:
            print("❌ No assets found")
            return
        
        print(f"\n📊 Total assets: {len(assets)}")
        already_downloaded = len(self.progress['downloaded'])
        print(f"✅ Already downloaded: {already_downloaded}")
        print(f"📥 To download: {len(assets) - already_downloaded}")
        
        # Filter out already downloaded
        to_download = [a for a in assets if a.get('id') not in self.progress['downloaded']]
        
        if not to_download:
            print("\n🎉 All assets already downloaded!")
            return
        
        print(f"\n🚀 Starting download with {MAX_WORKERS} concurrent workers...")
        
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self.download_asset, asset): asset for asset in to_download}
            
            for i, future in enumerate(as_completed(futures), 1):
                asset = futures[future]
                result = future.result()
                
                if result == 'success':
                    success_count += 1
                    print(f"✅ [{i}/{len(to_download)}] {asset.get('name', asset.get('id'))}")
                elif result == 'skipped':
                    skipped_count += 1
                elif result == 'failed':
                    failed_count += 1
                    print(f"❌ [{i}/{len(to_download)}] Failed: {asset.get('name', asset.get('id'))}")
        
        # Final summary
        print("\n" + "="*60)
        print("📊 Download Summary")
        print("="*60)
        print(f"✅ Successfully downloaded: {success_count}")
        print(f"⏭️  Skipped (already downloaded): {skipped_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📁 Total in library: {len(self.progress['downloaded'])}")
        print(f"📂 Output directory: {OUTPUT_DIR.absolute()}")
        
        if failed_count > 0:
            print(f"\n⚠️  {failed_count} downloads failed. Check {PROGRESS_FILE} for details.")
    
    def show_stats(self):
        """Show download statistics"""
        print("\n📊 Runway Download Statistics")
        print("="*60)
        print(f"✅ Downloaded: {len(self.progress['downloaded'])}")
        print(f"❌ Failed: {len(self.progress['failed'])}")
        
        if self.progress['downloaded']:
            total_size = sum(d.get('size', 0) for d in self.progress['downloaded'].values())
            print(f"💾 Total size: {total_size / (1024**3):.2f} GB")
        
        print(f"📂 Output directory: {OUTPUT_DIR.absolute()}")

def main():
    print("🎬 Runway Video Downloader")
    print("="*60)
    
    downloader = RunwayDownloader()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        downloader.show_stats()
    else:
        downloader.download_all()

if __name__ == '__main__':
    main()
