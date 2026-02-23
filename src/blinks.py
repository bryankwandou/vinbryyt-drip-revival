import json
import os

def generate_blink_metadata(drop_id, image_url):
    """
    Generates OrbitFlare/Solana Blinks compliant action metadata.
    """
    metadata = {
        "icon": image_url,
        "title": f"VinBryYT Revival #{drop_id}",
        "description": "Reviving digital souls on Solana. Support the autonomous artist!",
        "label": "Collect Art",
        "links": {
            "actions": [
                {
                    "label": "Tip Creator (0.01 SOL)",
                    "href": f"/api/actions/tip?amount=0.01&drop={drop_id}",
                    "parameters": []
                },
                {
                    "label": "Collect NFT",
                    "href": f"/api/actions/collect?drop={drop_id}",
                    "parameters": []
                }
            ]
        }
    }
    
    path = os.path.join("metadata", f"actions_{drop_id}.json")
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"✅ Blink metadata saved to: {path}")
    return path
