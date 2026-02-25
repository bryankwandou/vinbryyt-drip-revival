import json
import os

def generate_blink_metadata(asset_name, image_url):
    """
    Generates a Solana Actions (Blink) compliant JSON metadata.
    """
    blink_data = {
        "title": f"VinBryYT Revival: {asset_name}",
        "icon": image_url,
        "description": "Autonomous Cyber-Precision drop from Project Chronos. Support the revival.",
        "label": "Collect Drop",
        "links": {
            "actions": [
                {
                    "label": "Collect (0.01 SOL)",
                    "href": "/api/collect?amount=0.01",
                },
                {
                    "label": "Tip Creator",
                    "href": "/api/tip?amount={amount}",
                    "parameters": [
                        {
                            "name": "amount",
                            "label": "SOL Amount",
                        }
                    ],
                }
            ]
        }
    }
    
    file_path = f"metadata/blink_{asset_name.lower().replace(' ', '_')}.json"
    with open(file_path, "w") as f:
        json.dump(blink_data, f, indent=4)
    
    print(f"🔗 Blink Metadata generated: {file_path}")
    return file_path
