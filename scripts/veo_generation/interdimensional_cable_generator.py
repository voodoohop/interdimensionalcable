#!/usr/bin/env python3
"""
Interdimensional Cable Channel Generator
Creates surreal retrofuturist videos for Gaswerksiedlung's birthday celebration.
All videos start with the iconic CRT poster frame and transition into Stanislaw Lem-inspired content.
"""

import json
import time
import os
import random
import subprocess
import base64
import mimetypes
from datetime import datetime
from typing import List, Dict, Optional

class InterdimensionalCableGenerator:
    def __init__(self, project_id: str = "pollinations-430910"):
        self.project_id = project_id
        self.base_url = "https://us-central1-aiplatform.googleapis.com/v1"
        self.model = "veo-3.0-generate-001"
        self.init_images_dir = "init"
        
        # CRT poster opening frame - the iconic start for all videos
        self.crt_opening_frame = """
        16:9 retro CRT television screen displaying a vintage broadcast poster. 
        Two-line header at top in bold futurist sans-serif font, slightly arced to match screen curvature: 
        "GASWERKSIEDLUNG" on first line, "INTERDIMENSIONAL CABLE" on second line, both in bright green phosphor glow.
        Center: thin white outline icon of the distinctive Gaswerksiedlung industrial building with short cable stubs extending left and right, 
        positioned over a horizontal TV test-card color strip (red, green, blue, yellow bars).
        Bottom-left corner: date "27. SEPTEMBER 3023" in small retro digital font.
        Bottom-right corner: tiny four-point star symbol glowing softly.
        Analog CRT aesthetics: visible scanlines, subtle screen curvature, phosphor glow, mild VHS static noise, 
        slight chromatic aberration at edges. The screen has a warm amber tint typical of old monitors.
        Audio: Soft electronic hum, occasional static pops, faint retro synthesizer chord.
        """

    def get_access_token(self) -> Optional[str]:
        """Get access token using gcloud CLI."""
        try:
            result = subprocess.run(['/opt/homebrew/bin/gcloud', 'auth', 'print-access-token'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"❌ Failed to get access token: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Error getting access token: {e}")
            return None

    def encode_image_to_base64(self, image_path: str) -> Optional[Dict[str, str]]:
        """Encode a local image file to base64 for Veo 3 API usage."""
        try:
            if not os.path.exists(image_path):
                print(f"❌ Image file not found: {image_path}")
                return None
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(image_path)
            if mime_type not in ['image/jpeg', 'image/png']:
                print(f"❌ Unsupported image format: {mime_type}. Use JPEG or PNG.")
                return None
            
            # Read and encode image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
            
            return {
                'bytesBase64Encoded': base64_encoded,
                'mimeType': mime_type
            }
            
        except Exception as e:
            print(f"❌ Error encoding image {image_path}: {e}")
            return None

    def get_random_init_image(self) -> Optional[str]:
        """Get a random image from the init folder."""
        try:
            init_dir = os.path.join(os.getcwd(), self.init_images_dir)
            if not os.path.exists(init_dir):
                return None
            
            image_files = [f for f in os.listdir(init_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                return None
            
            selected_image = random.choice(image_files)
            return os.path.join(init_dir, selected_image)
            
        except Exception as e:
            print(f"❌ Error selecting random init image: {e}")
            return None

    def get_surreal_prompts(self) -> List[Dict[str, str]]:
        """Generate Stanislaw Lem-inspired surreal retrofuturist video prompts."""
        
        prompts = [
            {
                "title": "The Memory Synthesizer",
                "prompt": f"""
                {self.crt_opening_frame}
                
                The CRT screen flickers and the image dissolves into static. Through the interference, 
                a vast chrome laboratory materializes in grainy 1970s sci-fi film aesthetic. 
                A massive crystalline device with pulsing geometric patterns hovers in the center, 
                surrounded by floating holographic memory fragments - childhood scenes, alien landscapes, 
                impossible architectures. A figure in a retro-futuristic white suit approaches the device, 
                their reflection multiplied infinitely in the crystal facets. As they touch it, 
                the memories begin to merge and transform into new, impossible recollections.
                
                Visual style: Grainy 16mm film, desaturated colors with occasional neon highlights, 
                analog video artifacts, chromatic aberration. Slow, hypnotic camera movements.
                Audio: Deep synthesizer drones, crystalline chimes, whispered fragments of conversation 
                in unknown languages, subtle VHS tape hiss.
                """
            },
            {
                "title": "The Probability Garden",
                "prompt": f"""
                {self.crt_opening_frame}
                
                Static clears to reveal a bizarre botanical garden where plants exist in multiple 
                quantum states simultaneously. Trees phase between different species, flowers bloom 
                and wither in impossible time loops, and geometric hedges reshape themselves 
                according to mathematical equations. A gardener in vintage space suit tends to 
                probability roses that exist as translucent overlapping possibilities. 
                The sky shifts between different atmospheric compositions - sometimes Earth-like, 
                sometimes alien with multiple moons.
                
                Visual style: Retrofuturist 1960s aesthetic, multiple exposure effects, 
                translucent overlays, vintage color grading with heavy grain. 
                Stop-motion-like temporal stuttering.
                Audio: Organic growth sounds mixed with electronic bleeps, wind through impossible 
                geometries, distant radio transmissions from other dimensions.
                """
            },
            {
                "title": "The Bureaucracy of Dreams",
                "prompt": f"""
                {self.crt_opening_frame}
                
                The screen transitions to a surreal office complex where dreams are processed 
                as paperwork. Clerks in identical gray suits stamp and file floating dream bubbles 
                that contain swirling, abstract imagery. Conveyor belts carry nightmares in manila 
                folders past towering filing cabinets that stretch infinitely upward. 
                A supervisor with multiple arms efficiently sorts subconscious thoughts into 
                different categories. The architecture is impossible - stairs lead nowhere, 
                doors open to other doors, and gravity seems optional.
                
                Visual style: Monochromatic with occasional color highlights, German Expressionist 
                angles, vintage office equipment, analog video compression artifacts.
                Audio: Typewriter clicks, rubber stamps, paper shuffling, distant elevator music 
                played on a malfunctioning synthesizer, bureaucratic mumbling.
                """
            },
            {
                "title": "The Temporal Archaeologist",
                "prompt": f"""
                {self.crt_opening_frame}
                
                Through static interference, we see an archaeologist in retro-futuristic gear 
                excavating layers of time itself. Each archaeological layer reveals different eras 
                existing simultaneously - ancient ruins, medieval castles, industrial machinery, 
                and futuristic cities all stacked vertically. The archaeologist uses strange 
                temporal tools that phase through solid matter, collecting chronological artifacts 
                that flicker between different time periods. Fossilized moments hang in the air 
                like amber-trapped insects.
                
                Visual style: Sepia tones with temporal color bleeding, archaeological documentary 
                aesthetic mixed with sci-fi B-movie grain, multiple temporal exposures.
                Audio: Digging sounds, temporal echoes of different eras overlapping, 
                ancient chants mixed with futuristic electronic tones, crackling radio static.
                """
            },
            {
                "title": "The Emotion Factory",
                "prompt": f"""
                {self.crt_opening_frame}
                
                The CRT dissolves into a vast industrial complex where emotions are manufactured 
                on assembly lines. Workers in vintage hazmat suits operate bizarre machinery that 
                distills pure joy from rainbow-colored vapors, compresses anger into red crystalline 
                cubes, and bottles liquid melancholy in glass containers. Conveyor belts transport 
                different emotional states through pneumatic tubes. A quality control inspector 
                tests samples of artificial nostalgia using retro-futuristic instruments.
                
                Visual style: Industrial documentary meets 1970s sci-fi, muted colors with 
                emotional color coding, heavy grain and analog artifacts, steam and vapor effects.
                Audio: Industrial machinery, pneumatic hisses, emotional resonance tones, 
                factory ambience mixed with synthesized emotional frequencies.
                """
            },
            {
                "title": "The Solaris Communication Station",
                "prompt": f"""
                {self.crt_opening_frame}
                
                Static clears to reveal a communication station attempting to decode messages 
                from a sentient ocean planet. Massive analog computers with spinning tape reels 
                process incomprehensible data streams. The ocean's thoughts manifest as shifting 
                geometric patterns on multiple CRT monitors. A lone operator in vintage space gear 
                watches as the alien intelligence tries to communicate through mathematical 
                equations that transform into living, breathing symbols floating in the air.
                
                Visual style: 1970s space station aesthetic, multiple monitor displays, 
                analog computer interfaces, heavy film grain, phosphor green displays.
                Audio: Computer processing sounds, alien mathematical harmonics, 
                deep ocean-like resonances, vintage sci-fi electronic music.
                """
            },
            {
                "title": "The Metamorphosis Chamber",
                "prompt": f"""
                {self.crt_opening_frame}
                
                Through interference, a sterile medical facility appears where beings undergo 
                voluntary transformation into abstract concepts. Patients enter chrysalis-like 
                pods and emerge as living geometric shapes, mathematical equations, or pure 
                energy patterns. Medical staff in retro-futuristic uniforms monitor the process 
                using analog instruments with glowing dials. The transformations are beautiful 
                but unsettling, as humanity dissolves into pure information.
                
                Visual style: Clinical white with neon accents, medical documentary aesthetic, 
                analog video artifacts, transformation effects using practical techniques.
                Audio: Medical equipment beeps, transformation energy sounds, 
                whispered philosophical discussions, ambient medical facility atmosphere.
                """
            },
            {
                "title": "The Library of Unwritten Books",
                "prompt": f"""
                {self.crt_opening_frame}
                
                The screen reveals an infinite library where books write themselves. 
                Typewriters operate autonomously, creating stories that have never been imagined. 
                Books float through the air, their pages fluttering with self-generating text. 
                A librarian in vintage attire catalogs impossible narratives - stories that exist 
                only in potential, tales from parallel universes, and books that read their readers. 
                The architecture defies physics with impossible shelving systems and gravity-defying 
                reading areas.
                
                Visual style: Sepia library tones with magical realism, floating text effects, 
                vintage library aesthetic, analog film grain and artifacts.
                Audio: Typewriter keys, page turning, whispered stories in multiple languages, 
                the sound of ideas materializing, ambient library atmosphere.
                """
            }
        ]
        
        return prompts

    def generate_video(self, prompt: str, title: str, init_image_path: Optional[str] = None) -> Optional[str]:
        """Generate a single video using Veo 3."""
        import requests
        
        access_token = self.get_access_token()
        if not access_token:
            print("❌ Failed to get access token")
            return None
            
        url = f"{self.base_url}/projects/{self.project_id}/locations/us-central1/publishers/google/models/{self.model}:predictLongRunning"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Build the instance object
        instance = {"prompt": prompt}
        
        # Add image conditioning if provided
        if init_image_path:
            print(f"🖼️  Using init image: {os.path.basename(init_image_path)}")
            image_data = self.encode_image_to_base64(init_image_path)
            
            if image_data:
                # Use the simple image field for Veo 3 image-to-video
                instance["image"] = image_data
                print(f"✅ Image encoded successfully ({len(image_data['bytesBase64Encoded'])//1024}KB)")
            else:
                print("⚠️  Failed to encode image, proceeding with text-only generation")
        
        payload = {
            "instances": [instance],
            "parameters": {
                "durationSeconds": 8,
                "aspectRatio": "16:9",
                "generateAudio": True,
                "sampleCount": 1
            }
        }
        
        print(f"🎬 Generating: {title}")
        print(f"📝 Prompt length: {len(prompt)} characters")
        if init_image_path:
            print(f"🖼️  Init image: {os.path.basename(init_image_path)}")
        else:
            print("📝 Text-to-video generation (no init image)")
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                operation_name = result.get('name')
                print(f"✅ Started: {operation_name}")
                return operation_name
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None

    def check_operation_status(self, operation_name: str) -> Optional[Dict]:
        """Check the status of a video generation operation."""
        import requests
        
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"{self.base_url}/projects/{self.project_id}/locations/us-central1/publishers/google/models/{self.model}:fetchPredictOperation"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {"operationName": operation_name}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                is_done = result.get('done', False)
                
                if is_done:
                    print("✅ Video generation completed!")
                    videos = result.get('response', {}).get('videos', [])
                    for i, video in enumerate(videos):
                        print(f"🎥 Video {i+1}: {video.get('gcsUri', 'No URI available')}")
                else:
                    print("⏳ Still generating...")
                
                return result
            else:
                print(f"❌ Status check failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return None

    def generate_channel_lineup(self, num_videos: int = 5, use_init_images: bool = False) -> List[Dict]:
        """Generate a lineup of interdimensional cable videos."""
        prompts = self.get_surreal_prompts()
        selected_prompts = random.sample(prompts, min(num_videos, len(prompts)))
        
        operations = []
        
        print(f"🎭 INTERDIMENSIONAL CABLE CHANNEL")
        print(f"🎂 Gaswerksiedlung Birthday Special")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        for i, prompt_data in enumerate(selected_prompts, 1):
            print(f"\n📺 Program {i}/{len(selected_prompts)}: {prompt_data['title']}")
            
            # Get init image if requested
            init_image_path = None
            if use_init_images:
                init_image_path = self.get_random_init_image()
                if init_image_path:
                    print(f"🎨 Selected init image: {os.path.basename(init_image_path)}")
                else:
                    print("⚠️  No init images found, using text-only generation")
            
            operation_name = self.generate_video(prompt_data['prompt'], prompt_data['title'], init_image_path)
            
            if operation_name:
                operations.append({
                    'title': prompt_data['title'],
                    'operation_name': operation_name,
                    'status': 'generating',
                    'started_at': datetime.now().isoformat()
                })
                
                # Small delay between requests
                time.sleep(2)
            else:
                operations.append({
                    'title': prompt_data['title'],
                    'operation_name': None,
                    'status': 'failed',
                    'started_at': datetime.now().isoformat()
                })
        
        # Save operations to file for tracking
        with open('interdimensional_cable_operations.json', 'w') as f:
            json.dump(operations, f, indent=2)
        
        print(f"\n📊 Channel Lineup Summary:")
        print(f"✅ Successfully started: {len([op for op in operations if op['operation_name']])}")
        print(f"❌ Failed to start: {len([op for op in operations if not op['operation_name']])}")
        print(f"💾 Operations saved to: interdimensional_cable_operations.json")
        
        return operations

    def check_all_operations(self, operations_file: str = 'interdimensional_cable_operations.json', auto_download: bool = True) -> None:
        """Check status of all operations from a previous run."""
        try:
            with open(operations_file, 'r') as f:
                operations = json.load(f)
        except FileNotFoundError:
            print(f"❌ Operations file not found: {operations_file}")
            return
        
        print("🔍 Checking all operation statuses...")
        print("=" * 50)
        
        completed_count = 0
        newly_completed = []
        
        for operation in operations:
            if operation['operation_name']:
                print(f"\n📺 {operation['title']}")
                result = self.check_operation_status(operation['operation_name'])
                
                if result and result.get('done'):
                    if operation.get('status') != 'completed':
                        newly_completed.append((operation, result))
                    operation['status'] = 'completed'
                    completed_count += 1
                elif result:
                    operation['status'] = 'generating'
                else:
                    operation['status'] = 'error'
            else:
                print(f"\n📺 {operation['title']}: ❌ Failed to start")
        
        # Update the operations file
        with open(operations_file, 'w') as f:
            json.dump(operations, f, indent=2)
        
        print(f"\n📊 Status Summary:")
        print(f"✅ Completed: {completed_count}")
        print(f"⏳ Still generating: {len([op for op in operations if op['status'] == 'generating'])}")
        print(f"❌ Failed/Error: {len([op for op in operations if op['status'] in ['failed', 'error']])}")
        
        # Auto-download newly completed videos
        if auto_download and newly_completed:
            print(f"\n📥 Auto-downloading {len(newly_completed)} newly completed videos...")
            from video_downloader import VideoDownloader
            downloader = VideoDownloader()
            
            for operation, result in newly_completed:
                downloader.download_video_from_operation(result, operation['title'])

def main():
    """Main function with CLI interface."""
    import sys
    
    generator = InterdimensionalCableGenerator()
    
    if len(sys.argv) < 2:
        print("🎭 Interdimensional Cable Channel Generator")
        print("=" * 50)
        print("Usage:")
        print("  python interdimensional_cable_generator.py generate [num_videos] [--init-images]")
        print("  python interdimensional_cable_generator.py check")
        print("  python interdimensional_cable_generator.py test [--init-image path/to/image.jpg]")
        print("  python interdimensional_cable_generator.py download")
        print("  python interdimensional_cable_generator.py gallery")
        print("\nExamples:")
        print("  python interdimensional_cable_generator.py generate 3")
        print("  python interdimensional_cable_generator.py generate 5 --init-images")
        print("  python interdimensional_cable_generator.py test --init-image init/image.jpg")
        print("  python interdimensional_cable_generator.py check")
        print("  python interdimensional_cable_generator.py download")
        print("  python interdimensional_cable_generator.py gallery")
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        num_videos = 5
        use_init_images = False
        
        # Parse arguments
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--init-images":
                use_init_images = True
            elif arg.isdigit():
                num_videos = int(arg)
        
        generator.generate_channel_lineup(num_videos, use_init_images)
        
    elif command == "check":
        generator.check_all_operations()
        
    elif command == "test":
        # Generate just one test video
        prompts = generator.get_surreal_prompts()
        test_prompt = random.choice(prompts)
        
        # Check for --init-image flag
        init_image_path = None
        for i, arg in enumerate(sys.argv):
            if arg == "--init-image" and i + 1 < len(sys.argv):
                init_image_path = sys.argv[i + 1]
                break
        
        # If no specific image provided, try to get a random one
        if not init_image_path:
            init_image_path = generator.get_random_init_image()
        
        print("🧪 Testing with single video generation...")
        if init_image_path:
            print(f"🎨 Using init image: {os.path.basename(init_image_path)}")
        
        operation_name = generator.generate_video(test_prompt['prompt'], test_prompt['title'], init_image_path)
        
        if operation_name:
            print(f"\n⏳ Waiting 30 seconds before checking status...")
            time.sleep(30)
            generator.check_operation_status(operation_name)
    
    elif command == "download":
        # Download all completed videos
        from video_downloader import VideoDownloader
        downloader = VideoDownloader()
        downloader.download_from_operations_file('interdimensional_cable_operations.json')
        
    elif command == "gallery":
        # Create video gallery
        from video_downloader import VideoDownloader
        downloader = VideoDownloader()
        gallery_path = downloader.create_video_gallery()
        print(f"\n🎨 Open the gallery: {gallery_path}")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
