import os
import sys

from upload.upload_to_youtube import upload_to_youtube
from upload.upload_facebook import upload_to_facebook
from upload.upload_instagram import upload_to_instagram

def publish_all_platforms(video_path, thumbnail_path=None, title=None, description=None, tags=None):
    """
    Unified multi-platform publishing orchestrator for Pokémon Challenge runs:
    1. YouTube: Uploads video, sets custom thumbnail, appends to playlist.
    2. Facebook: Posts video to Page (if credentials provided).
    3. Instagram: Posts Reel (if credentials provided).
    """
    print("\n" + "=" * 65)
    print("🌐 MULTI-PLATFORM PUBLISHING PIPELINE (POKÉMON AI CHALLENGE)")
    print("=" * 65)

    results = {}

    # 1. YouTube Upload
    yt_res = upload_to_youtube(
        video_path=video_path,
        thumbnail_path=thumbnail_path,
        title=title,
        description=description,
        tags=tags
    )
    results["youtube"] = yt_res

    # 2. Facebook Upload
    fb_res = upload_to_facebook(
        video_path=video_path,
        title=title,
        description=description
    )
    results["facebook"] = fb_res

    # 3. Instagram Upload (if video URL available)
    if yt_res.get("status") == "success" and yt_res.get("url"):
        ig_res = upload_to_instagram(
            video_url=yt_res["url"],
            caption=f"{title}\n\nWatch full challenge: {yt_res['url']}"
        )
        results["instagram"] = ig_res
    else:
        results["instagram"] = {"status": "skipped", "platform": "instagram", "reason": "No public video URL"}

    print("\n" + "=" * 65)
    print("📊 MULTI-PLATFORM PUBLISHING SUMMARY:")
    for platform, res in results.items():
        st = res.get("status", "unknown").upper()
        print(f"  • {platform.capitalize():<12}: [{st}] - {res.get('url') or res.get('reason') or res.get('id', 'Done')}")
    print("=" * 65)

    return results

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    v_path = os.path.join(base_dir, "recordings", "pokemon_magikarp_challenge.mp4")
    t_path = os.path.join(base_dir, "recordings", "thumbnail.png")
    if os.path.exists(v_path):
        publish_all_platforms(v_path, t_path)
    else:
        print(f"Video file not found at {v_path}. Run generate_pokemon_video.py first.")
