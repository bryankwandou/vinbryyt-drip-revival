# 🤖 VinBryYT: Project Chronos (Project Revival Engine)

Official submission for **Solana Graveyard Hackathon 2026**. VinBryYT is a 100% autonomous digital art revival channel, powered by an advanced AI engine and integrated with Solana Blinks.

## 🦾 Technical Architecture

### 1. The Chronos Engine (`src/engine.py`)
- **Text Engine**: Powered by **Groq API (Llama-3.3-70b)**. It handles prompt engineering, community posts, and creative writing (Pantun & Quotes).
- **Image Engine**: Utilizes **Hugging Face Inference API** with the **FLUX.1-schnell** model to generate hyper-realistic, high-fidelity 8k visuals.
- **Autonomous Schedule**:
  - **On the hour (XX:00)**: Generates a new image drop, DRiP metadata, and Blink action.
  - **On the half-hour (XX:30)**: Generates a community update, Pantun, or motivational quote.

### 2. Solana Blinks Integration (`src/blinks.py`)
Every drop automatically generates **OrbitFlare (Blinks)** compliant JSON metadata. This allows users to "Tip Creator" or "Collect NFT" directly from any platform that supports Solana Blinks.

### 3. Smart Persistence
- **`database/history.json`**: Tracks generated themes and timestamps to ensure zero repetition in the drops.
- **`assets/` & `metadata/`**: Autonomous storage for images and Metaplex-standard metadata.

---

## 🚀 Deployment Instructions

### 1. Configure GitHub Secrets
Add the following secrets to your repository (**Settings > Secrets and Variables > Actions**):
- `OPENAI_API_KEY`: Your **Groq API Key** (mapped automatically).
- `HF_TOKEN`: Your **Hugging Face Read Token**.

### 2. Manual Activation
The engine runs automatically every 30 minutes. To test immediately:
1. Go to the **Actions** tab.
2. Select **Project Chronos Autonomy Engine**.
3. Click **Run workflow**.

---

**Built for the Future of Creative Autonomy on Solana.**
*Reviving the soul, one block at a time.*
