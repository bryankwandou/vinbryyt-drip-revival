import os
import time
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_organic_comment():
    """Generates a high-fidelity organic comment using Groq 3.3."""
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a tech-savvy Solana art collector. Generate a short, organic, and enthusiastic comment (max 10 words) for a high-fidelity digital art piece. Do not use generic bot language. Be cool."
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Engagement error: {e}")
        return "Absolute fire! 🔥 #Solana"

def execute_mass_engagement(count=100):
    """
    Demonstrates the logic for mass organic engagement.
    Generates 100 unique organic comments to prove scaling.
    """
    print(f"🚀 Initializing Project Chronos: Mass Engagement Protocol ({count} comments)")
    start_time = time.time()
    for i in range(count):
        comment = generate_organic_comment()
        print(f"🤖 Bot #{i+1} generated: \"{comment}\"")
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n✅ Mass Engagement Proof Complete.")
    print(f"⏱️ Generated {count} organic comments in {duration:.2f} seconds.")
    print("Ready for automated injection into DRiP Haus.")

if __name__ == "__main__":
    execute_mass_engagement(100)
