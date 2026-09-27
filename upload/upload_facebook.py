import os
import requests

def upload_to_facebook(video_path, title=None, description=None):
    """
    Publishes video to Facebook Page Graph API.
    Reads FB_PAGE_ACCESS_TOKEN and FB_PAGE_ID from GitHub Secrets / Env Vars.
    """
    token = os.getenv("FB_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FB_PAGE_ID")

    if not token or not page_id:
        print("[facebook] ℹ️ Skipping Facebook upload: FB_PAGE_ACCESS_TOKEN or FB_PAGE_ID not set.")
        return {"status": "skipped", "platform": "facebook", "reason": "No credentials"}

    print(f"[facebook] Initiating Facebook Video upload to Page {page_id}...")
    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
    
    payload = {
        "access_token": token,
        "title": title or "Can an AI Beat Pokémon with ONLY a Magikarp?!",
        "description": description or "Daily Pokémon AI Challenge Run. 1 HP Focus Sash Flail Sweep vs Champion Blue!"
    }

    try:
        with open(video_path, "rb") as f:
            files = {"source": f}
            response = requests.post(url, data=payload, files=files, timeout=300)
            data = response.json()
            if "id" in data:
                print(f"[facebook] ✅ Video published! Facebook Video ID: {data['id']}")
                return {"status": "success", "platform": "facebook", "id": data["id"]}
            else:
                print(f"[facebook] ❌ Upload failed: {data}")
                return {"status": "error", "platform": "facebook", "error": data}
    except Exception as e:
        print(f"[facebook] ❌ Request exception: {e}")
        return {"status": "error", "platform": "facebook", "error": str(e)}

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    v_path = os.path.join(base_dir, "recordings", "pokemon_magikarp_challenge.mp4")
    if os.path.exists(v_path):
        upload_to_facebook(v_path)
    else:
        print(f"[facebook] Video not found at {v_path}")
