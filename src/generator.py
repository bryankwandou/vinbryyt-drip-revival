import os
import json
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add the script's directory to sys.path to ensure imports work when run from root
sys.path.append(str(Path(__file__).parent))

from utils import ensure_dir

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
METADATA_DIR = "metadata"
ASSETS_DIR = "assets"

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_prompt():
    """Generates a dynamic prompt for the 'Revival' theme."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    base_prompt = (
        "High-fidelity digital art representing the 'Revival' theme. "
        "A cyberpunk landscape where nature is reclaiming a neon city, vibrant greenery growing over glass towers. "
        "Intricate details, cinematic lighting, 8k resolution, ethereal atmosphere."
    )
    return f"{base_prompt} [Unique ID: {date_str}]"

def generate_art(prompt):
    """Generates an image using OpenAI DALL-E 3."""
    print(f"Generating art with prompt: {prompt}")
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating art: {e}")
        return None

def save_image(url, filename):
    """Downloads and saves the image from the given URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            path = os.path.join(ASSETS_DIR, filename)
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved to: {path}")
            return path
    except Exception as e:
        print(f"Error saving image: {e}")
    return None

def create_metadata(image_filename, prompt):
    """Creates a DRiP-compliant cNFT metadata JSON file."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    metadata = {
        "name": f"VinBryYT Revival #{timestamp}",
        "symbol": "VBRY",
        "description": f"Autonomous Revival Art generated daily. Prompt: {prompt}",
        "seller_fee_basis_points": 500,
        "image": f"https://github.com/nayrbryanGaming/vinbryyt-drip-revival/blob/main/{ASSETS_DIR}/{image_filename}?raw=true",
        "attributes": [
            {"trait_type": "Theme", "value": "Revival"},
            {"trait_type": "Generator", "value": "VinBryYT AI Brain"},
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
    print(f"Metadata saved to: {path}")
    return path

def main():
    # Ensure directories exist
    ensure_dir(METADATA_DIR)
    ensure_dir(ASSETS_DIR)
    
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found. Please set it in your environment.")
        return

    prompt = generate_prompt()
    image_url = generate_art(prompt)
    
    if image_url:
        now = datetime.now()
        image_filename = f"revival_{now.strftime('%Y%m%d_%H%M%S')}.png"
        save_image(image_url, image_filename)
        create_metadata(image_filename, prompt)
        print("Pipeline execution completed successfully!")
    else:
        print("Pipeline failed at art generation step.")

if __name__ == "__main__":
    main()
