#!/usr/bin/env python3
"""
Veo 3 Init Image Prompts
Detailed prompts designed for each of the 6 init images with specific camera movements and styles.
"""

def get_init_image_prompts():
    """Get prompts organized by init image with multiple style variations."""
    
    prompts = {
        "init_01.jpeg": {
            "title_base": "The Circuit Shaman",
            "variations": [
                {
                    "title": "The Circuit Shaman - Mystical Rotation",
                    "prompt": """An 8-second, high-resolution cinematic video of a hyper-detailed Afrofuturistic man with a mohawk. His face is adorned with intricate, glowing green circuitry and his vest is crafted from a circuit board. A slow 360-degree rotation of the camera reveals a swirling, ethereal green and brown vortex in the background, with small, abstract human-like figures drifting within it. The mood is mystical and otherworldly. The audio should be a low, humming electronic drone with faint, echoing whispers."""
                },
                {
                    "title": "The Circuit Shaman - Powerful Close-Up",
                    "prompt": """A dramatic 8-second close-up video focusing on the face of an Afrofuturistic man. Glowing green circuits are embedded in his skin and pulse with a soft light. He slowly lifts his gaze to meet the camera. The background is a swirling digital consciousness of green and black data streams. The mood is powerful and intense. Include a subtle, deep synth bass sound that grows in intensity."""
                },
                {
                    "title": "The Circuit Shaman - Eerie Dolly Shot",
                    "prompt": """An 8-second dolly shot that moves slowly toward an Afrofuturistic man wearing a vest made of a circuit board. As the camera approaches, the small, indistinct human-like figures in the swirling green background become clearer and seem to reach out. The ambiance is eerie and mesmerizing. The only sound is a faint, high-pitched electronic frequency."""
                }
            ]
        },
        
        "init_02.jpeg": {
            "title_base": "The Shell Sorcerer",
            "variations": [
                {
                    "title": "The Shell Sorcerer - Heroic Zoom",
                    "prompt": """An 8-second, epic cinematic video of a powerful Afrofuturistic man with a mohawk, his face and body adorned with a combination of seashells and glowing blue circuits. The camera slowly zooms in on his determined and focused expression. The background is a swirling vortex of green and teal data streams. The mood is heroic and grand. The audio should be a rising, inspirational orchestral score with subtle electronic elements."""
                },
                {
                    "title": "The Shell Sorcerer - Contemplative Turn",
                    "prompt": """A medium shot, 8-second video of an Afrofuturistic man wearing intricate armor made of shells and circuit boards. He slowly turns his head to the side, as if listening to a distant sound. The swirling green and brown background gently pulses with a soft, warm light. The mood is contemplative and serene. The audio consists of the gentle lapping of waves mixed with soft, melodic chimes."""
                },
                {
                    "title": "The Shell Sorcerer - Majestic Pan",
                    "prompt": """An 8-second video with a low-angle shot, looking up at a proud Afrofuturistic man with a mohawk and cybernetic enhancements. The camera slowly pans up the length of his body, emphasizing his powerful and majestic stature against the swirling vortex background. The mood is awe-inspiring. A deep, resonant drum beat provides the soundtrack."""
                }
            ]
        },
        
        "init_03.jpeg": {
            "title_base": "The Beaded Oracle",
            "variations": [
                {
                    "title": "The Beaded Oracle - Spiritual Meditation",
                    "prompt": """An 8-second, tranquil video of a graceful Afrofuturistic man with a headpiece intricately woven from beads and shells. He slowly closes his eyes in a state of deep meditation. The abstract, ghost-like figures in the swirling green background drift gently and peacefully. The mood is spiritual and serene. The audio should be a calming ambient track with the soft, organic sound of rattling beads."""
                },
                {
                    "title": "The Beaded Oracle - Hypnotic Journey",
                    "prompt": """A tracking shot, 8-second video, following an Afrofuturistic man as he walks slowly through a vibrant, digital jungle. His elaborate shell and bead adornments are in sharp focus. The background is a mesmerizing blur of green and brown motion. The mood is rhythmic and hypnotic. The audio is a tribal drum beat with layered electronic textures."""
                },
                {
                    "title": "The Beaded Oracle - Artistic Focus Pull",
                    "prompt": """An 8-second, artistic video that utilizes a rack focus effect. The shot begins with a close-up on the intricate beadwork of the man's chest piece, then slowly and smoothly shifts focus to his calm and composed face. The swirling green background has a soft, out-of-focus, dreamlike glow. The mood is beautiful and contemplative. A single, sustained musical note plays throughout."""
                }
            ]
        },
        
        "init_04.jpeg": {
            "title_base": "The Twin Oracles",
            "variations": [
                {
                    "title": "The Twin Oracles - Cinematic Reveal",
                    "prompt": """An 8-second, cinematic wide shot of two mysterious Afrofuturistic figures. They wear massive, elaborate headpieces made of vintage television screens that flicker with images of a swirling, cosmic portal. The camera slowly pushes in on them as they stand still and silent in a vast, red rock desert canyon, surrounded by a crowd of people in colorful robes. The mood is mysterious and grand. The audio should be a low, rumbling drone and the faint sound of wind."""
                },
                {
                    "title": "The Twin Oracles - Ominous Gaze",
                    "prompt": """An 8-second video from the perspective of someone in the crowd, looking up at the two towering figures with television screen headpieces. The screens glow with a bright, blue light, casting long shadows across the canyon walls. The figures remain motionless, exuding an ominous and powerful presence. The audio is a tense, atmospheric soundscape with a deep, pulsating hum."""
                },
                {
                    "title": "The Twin Oracles - Dynamic Orbit",
                    "prompt": """A dynamic 8-second video where the camera circles the two figures. The images on their television screen headpieces shift and change, displaying different cosmic nebulae and distant galaxies. The crowd in the background can be seen murmuring and pointing in awe. The mood is energetic and futuristic. The audio is a complex mix of electronic music and the excited chatter of a crowd."""
                }
            ]
        },
        
        "init_05.jpeg": {
            "title_base": "The Circuit Queens",
            "variations": [
                {
                    "title": "The Circuit Queens - Intimate Gaze",
                    "prompt": """An 8-second video with a shallow depth of field, focusing on the face of the Afrofuturistic woman in the foreground. Her intricate circuit board headpiece glimmers in the soft light. She slowly turns and makes direct, confident eye contact with the camera. In the background, the second woman and the crowd are softly blurred. The mood is intimate and engaging. The audio is a simple, elegant piano melody."""
                },
                {
                    "title": "The Circuit Queens - Regal Pan",
                    "prompt": """A slow, sweeping 8-second pan across the two women, showcasing their elaborate and detailed circuit board headpieces and their elegant green and gold patterned robes. They stand with serene and confident expressions in a stunning red rock canyon. The mood is regal and elegant. The audio is a majestic orchestral piece with a choir."""
                },
                {
                    "title": "The Circuit Queens - High-Tech Close-Up",
                    "prompt": """An 8-second video that starts with an extreme close-up on the small, glowing screens within one of the headpieces, displaying lines of code. The camera then quickly zooms out to reveal the full scene of the two women standing proudly with their tribe in the canyon. The mood is a blend of high-tech and traditional. The audio is a mix of futuristic electronic sounds and traditional African singing."""
                }
            ]
        },
        
        "init_06.jpeg": {
            "title_base": "The Contemplative Engineer",
            "variations": [
                {
                    "title": "The Contemplative Engineer - Introspective Orbit",
                    "prompt": """An 8-second, moody video of a thoughtful Afrofuturistic man with a mohawk and a unique crop top made of shells and circuits. He is looking down, seemingly lost in deep thought. The camera slowly orbits him, capturing his introspective expression from different angles. The swirling green and brown background has a melancholic and atmospheric feel. The audio is a slow, somber cello piece."""
                },
                {
                    "title": "The Contemplative Engineer - Detailed Tilt",
                    "prompt": """An 8-second video where the camera slowly tilts down from the man's thoughtful face to his intricate top, which is adorned with a mix of seashells and electronic components. The light catches the different textures of the organic and technological materials. The swirling background gently pulses with a soft, ambient light. The mood is detailed and atmospheric. The audio is a subtle electronic hum and the sound of a gentle breeze."""
                },
                {
                    "title": "The Contemplative Engineer - Raw Emotion",
                    "prompt": """A handheld style, 8-second video, giving a sense of immediacy and raw realism. The camera has a slight, natural shake as it focuses on the man's face. He takes a slow, deep breath, his shoulders rising and falling. The swirling background seems to subtly shift and react to his movement. The mood is raw and emotional. The audio is simply the sound of his breathing and a faint, distant synth pad."""
                }
            ]
        }
    }
    
    return prompts

def get_all_prompt_variations():
    """Get all prompt variations as a flat list for random selection."""
    all_prompts = []
    prompts_by_image = get_init_image_prompts()
    
    for image_file, image_data in prompts_by_image.items():
        for variation in image_data["variations"]:
            all_prompts.append({
                "title": variation["title"],
                "prompt": variation["prompt"],
                "init_image": image_file,
                "base_character": image_data["title_base"]
            })
    
    return all_prompts

def get_prompts_for_image(image_filename):
    """Get all prompt variations for a specific init image."""
    prompts_by_image = get_init_image_prompts()
    return prompts_by_image.get(image_filename, {}).get("variations", [])

def get_random_prompt_for_image(image_filename):
    """Get a random prompt variation for a specific init image."""
    import random
    variations = get_prompts_for_image(image_filename)
    return random.choice(variations) if variations else None

if __name__ == "__main__":
    # Demo usage
    prompts = get_init_image_prompts()
    print("🎬 Veo Init Image Prompts")
    print("=" * 50)
    
    for image_file, data in prompts.items():
        print(f"\n📸 {image_file} - {data['title_base']}")
        print(f"   {len(data['variations'])} variations available")
    
    print(f"\n📊 Total: {len(get_all_prompt_variations())} prompt variations across 6 images")
