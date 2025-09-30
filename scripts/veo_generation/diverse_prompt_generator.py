#!/usr/bin/env python3
"""
Diverse Prompt Generator - Creative video prompts beyond cinematic characters
Explores different themes, styles, and visual approaches for Veo 3 generation
"""

import random
import json
import base64
import subprocess
import requests
import os
from datetime import datetime

# Diverse prompt categories
ABSTRACT_PROMPTS = [
    "Liquid mercury flowing upward against gravity, transforming into geometric crystalline structures, iridescent reflections, slow motion, ethereal lighting",
    "Floating geometric shapes morphing between dimensions, pastel color palette, dreamy atmosphere, particles dissolving into light beams",
    "Swirling galaxies of paint mixing in zero gravity, vibrant colors bleeding into each other, cosmic dance, mesmerizing patterns",
    "Digital rain falling upward, binary code transforming into butterflies, cyberpunk aesthetic, neon blues and greens",
    "Origami flowers blooming in reverse time, paper petals unfolding into flat sheets, minimalist white background, gentle shadows"
]

NATURE_SURREAL_PROMPTS = [
    "Giant mushrooms growing in fast-forward through a misty forest floor, bioluminescent spores floating, magical realism, golden hour lighting",
    "Underwater garden where coral grows like trees, fish swimming between branches, sunbeams filtering through water, peaceful ambiance",
    "Desert sand dunes shifting to reveal ancient clockwork mechanisms, steampunk elements emerging from earth, warm sunset colors",
    "Ice crystals forming intricate mandala patterns on a frozen lake surface, time-lapse crystallization, pristine arctic environment",
    "Clouds forming into architectural structures in the sky, floating cloud cities, soft pastel colors, dreamy atmosphere"
]

RETRO_FUTURISM_PROMPTS = [
    "1980s neon grid landscape extending to infinity, synthwave aesthetic, purple and pink gradients, retro computer graphics style",
    "Vintage robot assembly line from the 1950s, chrome and brass automatons, industrial steam, sepia-toned retrofuturism",
    "Art deco spaceship interior with brass controls and velvet seats, elegant 1920s luxury meets space travel, warm golden lighting",
    "Cassette tapes transforming into holographic data streams, VHS glitch effects, nostalgic technology evolution",
    "Retro TV screens displaying static that forms into portal doorways, vintage electronics come alive, analog meets digital"
]

MICROSCOPIC_WORLDS_PROMPTS = [
    "Journey through a drop of water revealing microscopic civilizations, tiny creatures building crystal cities, macro photography style",
    "Blood cells flowing through veins like a river system, medical visualization meets artistic interpretation, red and pink hues",
    "Pollen grains exploding in slow motion, releasing golden dust clouds, extreme macro detail, nature's hidden beauty",
    "Soap bubble surface tension creating rainbow oil-slick patterns, iridescent colors shifting, delicate membrane physics",
    "Salt crystals growing in geometric formations, time-lapse crystallization, laboratory aesthetic, scientific wonder"
]

ARCHITECTURAL_DREAMS_PROMPTS = [
    "Impossible Escher-like staircases that loop infinitely, people walking in all directions, mind-bending perspective, monochrome palette",
    "Glass cathedral filled with floating books, pages turning in the air, golden light streaming through stained glass, magical library",
    "Brutalist concrete structures growing organic vines, nature reclaiming architecture, post-apocalyptic beauty, moss and ivy",
    "Transparent buildings revealing their inner workings, glass architecture with visible infrastructure, modern minimalism",
    "Ancient temple ruins floating in space, stone columns drifting among stars, cosmic archaeology, ethereal lighting"
]

WEATHER_PHENOMENA_PROMPTS = [
    "Lightning captured in slow motion, electrical branches spreading through storm clouds, dramatic black and white, raw power of nature",
    "Tornado made of autumn leaves instead of debris, colorful spiral of red and gold foliage, whimsical natural disaster",
    "Hailstones falling upward into the sky, reverse precipitation, surreal weather phenomenon, dramatic storm lighting",
    "Fog rolling through city streets like a living entity, mysterious urban atmosphere, noir cinematography, moody lighting",
    "Aurora borealis dancing over a mirror lake, perfect reflections doubling the light display, serene arctic landscape"
]

def get_access_token():
    """Get Google Cloud access token"""
    result = subprocess.run(['/opt/homebrew/bin/gcloud', 'auth', 'print-access-token'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to get access token: {result.stderr}")
    return result.stdout.strip()

def encode_image_to_base64(image_path):
    """Encode image to base64 for Veo 3 API"""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type
            if image_path.lower().endswith('.png'):
                mime_type = 'image/png'
            else:
                mime_type = 'image/jpeg'
                
            return base64_encoded, mime_type
    except Exception as e:
        print(f"❌ Failed to encode image {image_path}: {e}")
        return None, None

def generate_video(prompt, title, init_image_path=None):
    """Generate a video using Veo 3 API"""
    access_token = get_access_token()
    
    # Prepare the request
    instances = [{"prompt": prompt}]
    
    # Add init image if provided
    if init_image_path and os.path.exists(init_image_path):
        base64_data, mime_type = encode_image_to_base64(init_image_path)
        if base64_data:
            instances[0]["image"] = {
                "bytesBase64Encoded": base64_data,
                "mimeType": mime_type
            }
            print(f"🖼️  Using init image: {init_image_path}")
        else:
            print(f"⚠️  Failed to encode init image, proceeding with text-only")
    
    payload = {
        "instances": instances,
        "parameters": {
            "durationSeconds": 8,
            "aspectRatio": "16:9",
            "generateAudio": True,
            "sampleCount": 1
        }
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/pollinations-430910/locations/us-central1/publishers/google/models/veo-3.0-generate-001:predictLongRunning"
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            operation_name = result.get('name')
            print(f"✅ Started: {operation_name}")
            return operation_name
        else:
            print(f"❌ Failed to start generation: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating video: {e}")
        return None

def get_random_init_image():
    """Get a random init image from the init folder"""
    init_folder = "init"
    if not os.path.exists(init_folder):
        return None
    
    image_files = [f for f in os.listdir(init_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        return None
    
    return os.path.join(init_folder, random.choice(image_files))

def generate_diverse_videos(count, use_init_images=False, category=None):
    """Generate diverse videos with different prompt styles"""
    
    # Combine all prompt categories
    all_prompts = {
        "abstract": ABSTRACT_PROMPTS,
        "nature_surreal": NATURE_SURREAL_PROMPTS,
        "retro_futurism": RETRO_FUTURISM_PROMPTS,
        "microscopic": MICROSCOPIC_WORLDS_PROMPTS,
        "architectural": ARCHITECTURAL_DREAMS_PROMPTS,
        "weather": WEATHER_PHENOMENA_PROMPTS
    }
    
    # Select prompts based on category or use all
    if category and category in all_prompts:
        selected_prompts = all_prompts[category]
        category_name = category.replace("_", " ").title()
    else:
        # Mix from all categories
        selected_prompts = []
        for cat_prompts in all_prompts.values():
            selected_prompts.extend(cat_prompts)
        category_name = "Mixed Styles"
    
    print(f"🎨 DIVERSE PROMPT GENERATOR")
    print(f"🎭 Category: {category_name}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    operations = []
    
    for i in range(count):
        # Select random prompt
        prompt = random.choice(selected_prompts)
        
        # Create title from first few words
        title_words = prompt.split()[:4]
        title = " ".join(title_words).replace(",", "")
        
        # Get init image if requested
        init_image = None
        if use_init_images:
            init_image = get_random_init_image()
        
        print(f"\n📺 Video {i+1}/{count}: {title}")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        if init_image:
            print(f"🖼️  Init Image: {init_image}")
        
        # Generate video
        operation_name = generate_video(prompt, title, init_image)
        
        if operation_name:
            operations.append({
                "title": title,
                "prompt": prompt,
                "operation_name": operation_name,
                "init_image": init_image,
                "category": category or "mixed",
                "started_at": datetime.now().isoformat()
            })
        
    # Save operations to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diverse_operations_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(operations, f, indent=2)
    
    print(f"\n📊 Generation Summary:")
    print(f"✅ Successfully started: {len(operations)}")
    print(f"❌ Failed to start: {count - len(operations)}")
    print(f"💾 Operations saved to: {filename}")
    
    return operations

def main():
    """Main function with CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 diverse_prompt_generator.py <count> [--init-images] [--category CATEGORY]")
        print("\nCategories:")
        print("  abstract, nature_surreal, retro_futurism, microscopic, architectural, weather")
        print("\nExamples:")
        print("  python3 diverse_prompt_generator.py 3")
        print("  python3 diverse_prompt_generator.py 5 --init-images")
        print("  python3 diverse_prompt_generator.py 4 --category abstract")
        return
    
    count = int(sys.argv[1])
    use_init_images = "--init-images" in sys.argv
    
    category = None
    if "--category" in sys.argv:
        try:
            cat_index = sys.argv.index("--category") + 1
            category = sys.argv[cat_index]
        except IndexError:
            print("❌ Please specify a category after --category")
            return
    
    generate_diverse_videos(count, use_init_images, category)

if __name__ == "__main__":
    main()
