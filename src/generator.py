import os
import json
import requests
import sys
from datetime import datetime
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

# Add the script's directory to sys.path
sys.path.append(str(Path(__file__).parent))
from utils import ensure_dir

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
METADATA_DIR = "metadata"
ASSETS_DIR = "assets"

def generate_prompt_with_groq():
    """Uses Groq to generate a highly detailed, unique Revival prompt."""
    if not GROQ_API_KEY:
        return "Nature reclaiming a cyberpunk city, 8k, ethereal"
        
    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Art Prompt Engineer. Create a short, highly descriptive (max 50 words) art prompt for the theme 'Revival'. Focus on nature overcoming technology, vibrant colors, and cinematic lighting."
                },
                {
                    "role": "user",
                    "content": f"Generate a unique revival prompt for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return "Nature reclaiming a cyberpunk city, 8k, ethereal"

def generate_art_pollinations(prompt):
    """Generates an image using Pollinations.ai (Free/No Key)."""
    print(f"🎨 Generating art with prompt: {prompt}")
    # URL encode the prompt
    encoded_prompt = requests.utils.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={datetime.now().timestamp()}&nologo=true"
    return image_url

def save_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            path = os.path.join(ASSETS_DIR, filename)
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Image saved to: {path}")
            return path
    except Exception as e:
        print(f"❌ Error saving image: {e}")
    return None

def create_metadata(image_filename, prompt):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    metadata = {
        "name": f"VinBryYT Revival #{timestamp}",
        "symbol": "VBRY",
        "description": f"Autonomous Revival Art. Prompt: {prompt}",
        "seller_fee_basis_points": 500,
        "image": f"https://github.com/nayrbryanGaming/vinbryyt-drip-revival/blob/main/{ASSETS_DIR}/{image_filename}?raw=true",
        "attributes": [
            {"trait_type": "Theme", "value": "Revival"},
            {"trait_type": "Generator", "value": "VinBryYT Groq-Pollination Brain"},
            {"trait_type": "Date", "value": now.strftime("%Y-%m-%d")}
        ],
        "properties": {
            "files": [
                {
                    "uri": f"https://github.com/nayrbryanGaming/vinbryyt-drip-revival/blob/main/{ASSETS_DIR}/{image_filename}?raw=true",
                    "type": "image/png"
                }
            ],
            "category": "image"
        }
    }
    
    metadata_filename = f"metadata_{timestamp}.json"
    path = os.path.join(METADATA_DIR, metadata_filename)
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"✅ Metadata saved to: {path}")
    return path

def main():
    ensure_dir(METADATA_DIR)
    ensure_dir(ASSETS_DIR)
    
    prompt = generate_prompt_with_groq()
    image_url = generate_art_pollinations(prompt)
    
    if image_url:
        now = datetime.now()
        image_filename = f"revival_{now.strftime('%Y%m%d_%H%M%S')}.png"
        if save_image(image_url, image_filename):
            create_metadata(image_filename, prompt)
            print("🚀 Pipeline execution completed successfully!")
        else:
            print("❌ Failed to save image.")
    else:
        print("❌ Failed to generate image URL.")

if __name__ == "__main__":
    main()
