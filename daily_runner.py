import asyncio
import os
import sys

from generate_pokemon_video import generate_pokemon_video, OUTPUT_VIDEO
from thumbnail_generator import generate_youtube_thumbnail
from upload.publisher import publish_all_platforms

async def run_daily_pokemon_pipeline():
    """
    Complete end-to-end autonomous daily runner:
    1. Generates 1080p 60FPS battle video with dual-character commentary.
    2. Generates high-CTR thumbnail.
    3. Publishes to YouTube (with playlist & SEO), Facebook, and Instagram.
    """
    print("\n" + "#" * 70)
    print("      DAILY POKÉMON AI CHALLENGE RUNNER: STARTING PIPELINE")
    print("#" * 70 + "\n")

    # 1. Generate Pokémon Challenge Video
    print("[STEP 1/3] Rendering Pokémon Challenge Battle Video (1080p 60FPS)...")
    video_path = await generate_pokemon_video()

    # 2. Generate / Verify High-CTR Thumbnail
    print("\n[STEP 2/3] Generating High-CTR Viral Thumbnail...")
    thumbnail_path = generate_youtube_thumbnail()

    # 3. Publish to YouTube, Facebook, Instagram
    print("\n[STEP 3/3] Uploading and Publishing Across All Platforms...")
    title = "Can an AI Beat Pokémon with ONLY a Magikarp?! (1 HP Focus Sash Solo Sweep)"
    description = (
        "Can an AI beat Pokémon with ONLY a single Magikarp?\n\n"
        "In this hardcore challenge run, our competitive AI minimax engine pilots a Level 100 Magikarp "
        "against Champion Blue's full Indigo Plateau squad (Pidgeot, Alakazam, Rhydon, Exeggutor, Gyarados, Charizard).\n\n"
        "By abusing Focus Sash endure mechanics and surviving with exactly 1 HP, Magikarp unleashes 200 Base Power Flail "
        "to execute a 100% mathematically calculated solo sweep!\n\n"
        "🔥 Subscribe for daily AI gaming challenges!\n"
        "🎮 Playlist: Pokémon AI Challenge Runs"
    )
    tags = [
        "Pokemon", "Pokemon AI", "Magikarp", "Magikarp Solo Run",
        "Pokemon Challenge", "Pokemon FireRed", "Focus Sash", "Flail",
        "Pokemon Champion", "Gaming AI", "AI Plays Pokemon", "Competitive Pokemon"
    ]

    results = publish_all_platforms(
        video_path=video_path,
        thumbnail_path=thumbnail_path,
        title=title,
        description=description,
        tags=tags
    )

    print("\n" + "#" * 70)
    print("      DAILY POKÉMON PIPELINE COMPLETED SUCCESSFULLY!")
    print("#" * 70 + "\n")

if __name__ == "__main__":
    asyncio.run(run_daily_pokemon_pipeline())
