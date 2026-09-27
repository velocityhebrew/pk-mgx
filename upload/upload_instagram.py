import os
import requests

def upload_to_instagram(video_url, caption=None):
    """
    Publishes video / Reel to Instagram Graph API via a public media container URL.
    Reads IG_ACCESS_TOKEN and IG_USER_ID from GitHub Secrets / Env Vars.
    """
    token = os.getenv("IG_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    ig_user_id = os.getenv("IG_USER_ID")

    if not token or not ig_user_id:
        print("[instagram] ℹ️ Skipping Instagram upload: IG_ACCESS_TOKEN or IG_USER_ID not set.")
        return {"status": "skipped", "platform": "instagram", "reason": "No credentials"}

    print(f"[instagram] Initiating Instagram Reel upload for User ID {ig_user_id}...")
    container_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    
    payload = {
        "access_token": token,
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption or "Can an AI beat Pokémon with ONLY a Magikarp?! 1 HP Focus Sash Sweep! #pokemon #gaming #ai"
    }

    try:
        res = requests.post(container_url, data=payload, timeout=60).json()
        container_id = res.get("id")
        if not container_id:
            print(f"[instagram] ❌ Container creation failed: {res}")
            return {"status": "error", "platform": "instagram", "error": res}

        # Publish the container
        publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
        pub_res = requests.post(publish_url, data={"creation_id": container_id, "access_token": token}, timeout=60).json()
        if "id" in pub_res:
            print(f"[instagram] ✅ Reel published! Instagram Media ID: {pub_res['id']}")
            return {"status": "success", "platform": "instagram", "id": pub_res["id"]}
        else:
            print(f"[instagram] ❌ Publish failed: {pub_res}")
            return {"status": "error", "platform": "instagram", "error": pub_res}
    except Exception as e:
        print(f"[instagram] ❌ Request exception: {e}")
        return {"status": "error", "platform": "instagram", "error": str(e)}
