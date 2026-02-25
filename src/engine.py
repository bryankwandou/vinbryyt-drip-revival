import os
import json
import random
import requests
import time
from datetime import datetime
from groq import Groq
from src.blinks import generate_blink_metadata
from dotenv import load_dotenv

load_dotenv()

# API Clients
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
client = Groq(api_key=GROQ_API_KEY)

# Constants
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

THEMES = [
    "Cyberpunk Landscapes", 
    "Hyper-realistic Supercars", 
    "Abstract Solana Aesthetics", 
    "Futuristic Architecture"
]

def query_hf(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"HF API Error: {response.text}")
    return response.content

def load_history():
    if not os.path.exists("database/history.json"):
        return {"image_themes": [], "last_run": None}
    with open("database/history.json", "r") as f:
        return json.load(f)

def save_history(history):
    with open("database/history.json", "w") as f:
        json.dump(history, f, indent=4)

def generate_hourly_drop():
    """Generates an image drop: Optimized prompt -> FLUX.1 -> Metadata -> Blinks."""
    print("🎨 Initializing Hourly Image Drop...")
    history = load_history()
    
    # Theme selection logic with repetition avoidance
    available_themes = [t for t in THEMES if t not in history["image_themes"]]
    if not available_themes:
        available_themes = THEMES
        history["image_themes"] = []
        
    theme = random.choice(available_themes)
    history["image_themes"].append(theme)
    save_history(history)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    asset_name = f"Chronos_{timestamp}"
    
    # 1. Use Groq to generate high-fidelity technical prompt
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a master technical prompt engineer for FLUX.1. Generate a 200-word cinematic, high-fidelity prompt. Focus on sharp detail, zero distortion, and cyber-precision aesthetics."
                },
                {
                    "role": "user",
                    "content": f"Create a technical prompt for a {theme} visual in 8k quality with Solana purple/cyan lighting."
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        technical_prompt = completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        technical_prompt = f"Futuristic {theme}, 8k, cinematic lighting."

    # 2. Generate Image via HF
    print(f"🚀 Generating Asset: {asset_name} with theme: {theme}")
    image_bytes = query_hf({"inputs": technical_prompt})
    image_path = f"assets/{asset_name}.png"
    with open(image_path, "wb") as f:
        f.writelines([image_bytes])

    # 3. Create DRiP Metadata
    drip_metadata = {
        "name": f"VinBryYT Revival #{timestamp}",
        "symbol": "VBRV",
        "description": f"An autonomous creative drop from Project Chronos. Theme: {theme}",
        "image": f"https://raw.githubusercontent.com/nayrbryanGaming/vinbryyt-drip-revival/main/assets/{asset_name}.png",
        "attributes": [{"trait_type": "Theme", "value": theme}, {"trait_type": "Engine", "value": "Project Chronos"}]
    }
    with open(f"metadata/{asset_name}.json", "w") as f:
        json.dump(drip_metadata, f, indent=4)

    # 4. Generate Blinks Link
    generate_blink_metadata(asset_name, drip_metadata["image"])
    print(f"✅ Hourly drop complete: {image_path}")

def generate_social_post():
    """Generates a revival-themed social post using Groq."""
    print("📝 Generating Community Post...")
    post_types = ["Pantun", "Motivational Quote", "System Status"]
    chosen_type = random.choice(post_types)
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Project Chronos, an autonomous AI entity on Solana. Generate a short, cool community post relating to 'Revival' or 'Cyber-Precision'."
                },
                {
                    "role": "user",
                    "content": f"Generate a {chosen_type} (Indonesian if Pantun, English otherwise)."
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        )
        post_content = completion.choices[0].message.content
        final_post = f"{post_content}\n\n#Solana #DRiP #VinBryYT"
    except Exception as e:
        final_post = "Project Chronos is active. The revival continues. #Solana #DRiP"

    with open("community_posts.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {final_post}\n---\n")
    
    print(f"🤖 Social Post Generated: {final_post[:50]}...")

if __name__ == "__main__":
    import sys
    # Ensure database exists
    if not os.path.exists("database"):
        os.makedirs("database")
    if not os.path.exists("assets"):
        os.makedirs("assets")
    if not os.path.exists("metadata"):
        os.makedirs("metadata")
        
    mode = sys.argv[1] if len(sys.argv) > 1 else "post"
    if mode == "image":
        generate_hourly_drop()
    else:
        generate_social_post()
