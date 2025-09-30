#!/usr/bin/env python3
"""
Enhanced Interdimensional Cable Generator with Veo Init Image Prompts
Combines the original surreal prompts with new cinematic init image prompts.
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
from veo_init_image_prompts import get_init_image_prompts, get_all_prompt_variations, get_random_prompt_for_image

class EnhancedInterdimensionalCableGenerator:
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

    def get_available_init_images(self) -> List[str]:
        """Get list of available init images."""
        try:
            init_dir = os.path.join(os.getcwd(), self.init_images_dir)
            if not os.path.exists(init_dir):
                return []
            
            image_files = [f for f in os.listdir(init_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            return sorted(image_files)
            
        except Exception as e:
            print(f"❌ Error listing init images: {e}")
            return []

    def get_random_init_image(self) -> Optional[str]:
        """Get a random image from the init folder."""
        image_files = self.get_available_init_images()
        if not image_files:
            return None
        
        selected_image = random.choice(image_files)
        return os.path.join(self.init_images_dir, selected_image)

    def get_surreal_prompts(self) -> List[Dict[str, str]]:
        """Generate original Stanislaw Lem-inspired surreal retrofuturist video prompts."""
        
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
                        if isinstance(video, dict) and 'bytesBase64Encoded' in video:
                            print(f"🎥 Video {i+1}: Base64 encoded ({len(video['bytesBase64Encoded'])//1024}KB)")
                        else:
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

    def generate_cinematic_lineup(self, num_videos: int = 3, specific_image: Optional[str] = None) -> List[Dict]:
        """Generate videos using the new cinematic init image prompts."""
        operations = []
        
        print(f"🎭 CINEMATIC INTERDIMENSIONAL CABLE")
        print(f"🎂 Gaswerksiedlung Birthday Special - Veo Edition")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get available images
        available_images = self.get_available_init_images()
        if not available_images:
            print("❌ No init images found!")
            return operations
        
        # Get all cinematic prompts
        all_prompts = get_all_prompt_variations()
        
        if specific_image:
            # Filter prompts for specific image
            filtered_prompts = [p for p in all_prompts if p['init_image'] == specific_image]
            if not filtered_prompts:
                print(f"❌ No prompts found for image: {specific_image}")
                return operations
            selected_prompts = random.sample(filtered_prompts, min(num_videos, len(filtered_prompts)))
        else:
            # Random selection from all prompts
            selected_prompts = random.sample(all_prompts, min(num_videos, len(all_prompts)))
        
        for i, prompt_data in enumerate(selected_prompts, 1):
            print(f"\n📺 Program {i}/{len(selected_prompts)}: {prompt_data['title']}")
            print(f"🎨 Character: {prompt_data['base_character']}")
            print(f"🖼️  Init Image: {prompt_data['init_image']}")
            
            init_image_path = os.path.join(self.init_images_dir, prompt_data['init_image'])
            
            operation_name = self.generate_video(
                prompt_data['prompt'], 
                prompt_data['title'], 
                init_image_path
            )
            
            if operation_name:
                operations.append({
                    'title': prompt_data['title'],
                    'operation_name': operation_name,
                    'status': 'generating',
                    'started_at': datetime.now().isoformat(),
                    'init_image': prompt_data['init_image'],
                    'base_character': prompt_data['base_character'],
                    'prompt_type': 'cinematic'
                })
                
                # Small delay between requests
                time.sleep(2)
            else:
                operations.append({
                    'title': prompt_data['title'],
                    'operation_name': None,
                    'status': 'failed',
                    'started_at': datetime.now().isoformat(),
                    'init_image': prompt_data['init_image'],
                    'base_character': prompt_data['base_character'],
                    'prompt_type': 'cinematic'
                })
        
        # Save operations to file
        operations_file = f'cinematic_operations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(operations_file, 'w') as f:
            json.dump(operations, f, indent=2)
        
        print(f"\n📊 Cinematic Lineup Summary:")
        print(f"✅ Successfully started: {len([op for op in operations if op['operation_name']])}")
        print(f"❌ Failed to start: {len([op for op in operations if not op['operation_name']])}")
        print(f"💾 Operations saved to: {operations_file}")
        
        return operations

def main():
    """Enhanced CLI interface."""
    import sys
    
    generator = EnhancedInterdimensionalCableGenerator()
    
    if len(sys.argv) < 2:
        print("🎭 Enhanced Interdimensional Cable Generator")
        print("=" * 50)
        print("Commands:")
        print("  cinematic [num] [--image init_XX.jpeg]  - Generate with cinematic prompts")
        print("  classic [num] [--init-images]           - Generate with classic surreal prompts")
        print("  test-cinematic [--image init_XX.jpeg]   - Test single cinematic video")
        print("  list-images                             - Show available init images")
        print("  show-prompts [init_XX.jpeg]             - Show prompts for specific image")
        print("\nExamples:")
        print("  python enhanced_generator.py cinematic 3")
        print("  python enhanced_generator.py cinematic 2 --image init_01.jpeg")
        print("  python enhanced_generator.py test-cinematic --image init_05.jpeg")
        print("  python enhanced_generator.py list-images")
        print("  python enhanced_generator.py show-prompts init_03.jpeg")
        return
    
    command = sys.argv[1]
    
    if command == "cinematic":
        num_videos = 3
        specific_image = None
        
        # Parse arguments
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg == "--image" and i + 1 < len(sys.argv):
                specific_image = sys.argv[i + 1]
            elif arg.isdigit():
                num_videos = int(arg)
        
        generator.generate_cinematic_lineup(num_videos, specific_image)
    
    elif command == "test-cinematic":
        specific_image = None
        
        # Check for --image flag
        for i, arg in enumerate(sys.argv):
            if arg == "--image" and i + 1 < len(sys.argv):
                specific_image = sys.argv[i + 1]
                break
        
        if not specific_image:
            # Pick random image
            available_images = generator.get_available_init_images()
            if available_images:
                specific_image = random.choice(available_images)
            else:
                print("❌ No init images available!")
                return
        
        # Get random prompt for the image
        prompt_data = get_random_prompt_for_image(specific_image)
        if not prompt_data:
            print(f"❌ No prompts available for {specific_image}")
            return
        
        print("🧪 Testing cinematic generation...")
        print(f"🎨 Character: {prompt_data['title']}")
        print(f"🖼️  Image: {specific_image}")
        
        init_image_path = os.path.join(generator.init_images_dir, specific_image)
        operation_name = generator.generate_video(
            prompt_data['prompt'], 
            prompt_data['title'], 
            init_image_path
        )
        
        if operation_name:
            print(f"\n⏳ Waiting 30 seconds before checking status...")
            time.sleep(30)
            generator.check_operation_status(operation_name)
    
    elif command == "list-images":
        images = generator.get_available_init_images()
        print("🖼️  Available Init Images:")
        print("=" * 30)
        for img in images:
            prompts_data = get_init_image_prompts().get(img, {})
            title = prompts_data.get('title_base', 'Unknown')
            variations = len(prompts_data.get('variations', []))
            print(f"📸 {img} - {title} ({variations} prompts)")
    
    elif command == "show-prompts":
        if len(sys.argv) < 3:
            print("❌ Please specify an image file")
            return
        
        image_file = sys.argv[2]
        prompts_data = get_init_image_prompts().get(image_file, {})
        
        if not prompts_data:
            print(f"❌ No prompts found for {image_file}")
            return
        
        print(f"🎬 Prompts for {image_file}")
        print(f"🎨 Character: {prompts_data['title_base']}")
        print("=" * 50)
        
        for i, variation in enumerate(prompts_data['variations'], 1):
            print(f"\n{i}. {variation['title']}")
            print(f"   {variation['prompt'][:100]}...")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
