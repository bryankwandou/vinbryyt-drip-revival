# 🚀 VinBryYT: Autonomous Solana DRiP Revival Pipeline

VinBryYT is a 100% autonomous digital art revival channel, built for the **Solana Graveyard Hackathon 2026**. This repository contains a fully automated pipeline that generates high-fidelity AI art and DRiP-compliant cNFT metadata daily.

## 🛠 Technical Implementation

### 1. The AI Brain (`src/generator.py`)
The core engine is a Python script that leverages **OpenAI DALL-E 3** to create unique "Revival" themed artwork. 
- **Dynamic Prompting:** Generates a fresh prompt every 24 hours with cryptographic-style timestamps to ensure stylistic variety.
- **DRiP cNFT Schema:** Automatically formats metadata into a standardized JSON structure that includes symbol (`VBRY`), royalty basis points, and relative image links.

### 2. The Automation Engine (`.github/workflows/daily_revival.yml`)
Powered by **GitHub Actions**, the pipeline runs on a daily CRON schedule (00:00 UTC).
- **Environment Management:** Uses GitHub Secrets to securely store the `OPENAI_API_KEY`.
- **Autonomous Persistence:** After generation, the bot automatically commits the new image (`/assets`) and metadata (`/metadata`) back to the main branch.

### 3. Solana Integration
The generated metadata follows the Metaplex standard used by DRiP, making these assets ready for minting as compressed NFTs (cNFTs) on the Solana blockchain.

---

## 🚀 Deployment Instructions

### 1. Configure Secrets
1. Go to your GitHub Repository: `nayrbryanGaming/vinbryyt-drip-revival`.
2. Navigate to **Settings > Secrets and Variables > Actions**.
3. Click **New repository secret**.
4. Name: `OPENAI_API_KEY`.
5. Value: Your OpenAI API Key (starts with `sk-...`).

### 2. Manual Test Run
1. Navigate to the **Actions** tab in your repository.
2. Select **Daily Revival Art Pipeline** on the left.
3. Click the **Run workflow** dropdown.
4. Click the green **Run workflow** button.

### 3. Verification
- Once the action completes, check the `assets/` folder for a new `.png`.
- Check the `metadata/` folder for a matching `.json`.

---

**Developed for Solana Graveyard Hackathon 2026**
*Reviving the digital soul, one block at a time.*
