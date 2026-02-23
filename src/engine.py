import os
import json
import random
import requests
import sys
from datetime import datetime
from groq import Groq
from huggingface_hub import InferenceClient
from pathlib import Path
from dotenv import load_dotenv

# Add script dir to path
sys.path.append(str(Path(__file__).parent))
from blinks import generate_blink_metadata
from utils import ensure_dir

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Constants
ASSETS_DIR = "assets"
METADATA_DIR = "metadata"
DATABASE_DIR = "database"
HISTORY_FILE = os.path.join(DATABASE_DIR, "history.json")

# Clients
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
hf_client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else None

THEMES = [
    "Cyberpunk Landscapes",
    "Hyper-realistic Supercars",
    "Abstract Solana Aesthetics",
    "Futuristic Architecture"
]

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def update_history(drop_id, theme, prompt):
    history = get_history()
    history[drop_id] = {
        "timestamp": str(datetime.now()),
        "theme": theme,
        "prompt": prompt
    }
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_social_post():
    """Generates a community post using Groq (Llama-3-8b)."""
    if not groq_client: return "System Status: Online. #VinBryYT"
    
    post_types = ["Pantun (Indonesian poetry)", "Motivational Quote", "System Status Update"]
    post_type = random.choice(post_types)
    
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are an AI community manager for VinBryYT. "
                        "Generate a short, engaging community post (max 50 words) about 'Revival' and digital art. "
                        "If the type is Pantun, use Indonesian. If others, use English. "
                        "End with #Solana #DRiP #VinBryYT."
                    )
                },
                {"role": "user", "content": f"Generate a {post_type} for the community."}
            ],
            model="llama3-8b-8192",
        )
        post = completion.choices[0].message.content
        with open("community_posts.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now()} ---\nType: {post_type}\n{post}\n")
        print(f"📝 Social post generated: {post_type}")
        return post
    except Exception as e:
        print(f"Groq Social Error: {e}")
        return "Reviving the past, building the future. #Solana #DRiP #VinBryYT"

def generate_hourly_drop():
    """Full drop: Image + Metadata + Blinks + History."""
    if not groq_client or not hf_client:
        print("Required API keys missing (GROQ_API_KEY/OPENAI_API_KEY or HF_TOKEN).")
        return

    # Filter themes based on history to ensure repetition-free drops
    history = get_history()
    recent_themes = [h.get("theme") for h in list(history.values())[-3:]] # Last 3 themes
    available_themes = [t for t in THEMES if t not in recent_themes]
    
    if not available_themes: available_themes = THEMES # Reset if all used
    theme = random.choice(available_themes)
    
    drop_id = datetime.now().strftime("%Y%m%d_%H%M")
    
    print(f"🚀 Starting Hourly Drop: {theme} (ID: {drop_id})")

    # 1. Groq Prompt Engineering (Llama-3-8b)
    try:
        prompt_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a master of technical art prompts. "
                        "Transform the theme into a 200-word highly detailed prompt for the FLUX.1 generative model. "
                        "Focus on 8k, zero distortion, high-fidelity visuals, cinematic lighting, and sharp textures. "
                        "Ensure the output is JUST the prompt text."
                    )
                },
                {"role": "user", "content": f"Theme: {theme}"}
            ],
            model="llama3-8b-8192",
        )
        technical_prompt = prompt_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Prompt Error: {e}")
        technical_prompt = f"A masterpiece of {theme}, hyper-detailed digital art revival style, high fidelity, 8k"

    # 2. FLUX.1 Image Generation (black-forest-labs/FLUX.1-schnell)
    try:
        print(f"🎨 Generating image for theme: {theme}")
        image = hf_client.text_to_image(
            technical_prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )
        img_path = os.path.join(ASSETS_DIR, f"drop_{drop_id}.png")
        image.save(img_path)
        print(f"✅ Image saved: {img_path}")
    except Exception as e:
        print(f"HF Generation Error: {e}")
        return

    # 3. DRiP Metadata
    image_url = f"https://github.com/nayrbryanGaming/vinbryyt-drip-revival/blob/main/{img_path}?raw=true"
    drip_metadata = {
        "name": f"VinBryYT Chronos #{drop_id}",
        "symbol": "VBRY",
        "description": f"Theme: {theme}. Prompt: {technical_prompt[:100]}...",
        "image": image_url,
        "attributes": [{"trait_type": "Theme", "value": theme}],
        "properties": {"files": [{"uri": image_url, "type": "image/png"}], "category": "image"}
    }
    
    metadata_path = os.path.join(METADATA_DIR, f"metadata_{drop_id}.json")
    with open(metadata_path, 'w') as f:
        json.dump(drip_metadata, f, indent=4)
        
    # 4. Blinks Integration
    generate_blink_metadata(drop_id, image_url)
    
    # 5. Track History
    update_history(drop_id, theme, technical_prompt)
    print(f"🚀 Hourly Drop #{drop_id} Complete!")

def main():
    """
    Project Chronos Master Scheduler logic.
    - XX:00 -> generate_hourly_drop()
    - XX:30 -> generate_social_post()
    """
    ensure_dir(ASSETS_DIR)
    ensure_dir(METADATA_DIR)
    ensure_dir(DATABASE_DIR)
    
    minute = datetime.now().minute
    
    # Logic for 30-minute schedule
    # 0-15: Hourly Drop (Image + Blink)
    # 30-45: Social Post Only
    # Others (manual): Run both for demo purposes
    
    if minute < 15:
        generate_hourly_drop()
    elif 30 <= minute < 45:
        generate_social_post()
    else:
        # Manual trigger or unexpected time: Do both for maximum yield
        print("⚡ Manual Trigger Detected: Executing Dual Chronos Protocol")
        generate_hourly_drop()
        generate_social_post()

if __name__ == "__main__":
    main()
