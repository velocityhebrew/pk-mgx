import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Fallback local token locations
LOCAL_TOKEN_PATHS = [
    r"C:\Users\kreg9\Downloads\kreggscode\open code\bots\youtube refresh tokens bot\token_chess magix.json",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "token.json")
]

DEFAULT_PLAYLIST_TITLE = "Pokémon AI Challenge Runs [Hardcore & Solo Battler]"

def get_authenticated_service():
    """Authenticate via GitHub Secrets / Env Vars or local token file."""
    client_id = (os.getenv('YOUTUBE_CLIENT_ID') or os.getenv('YT_CLIENT_ID', '')).strip()
    client_secret = (os.getenv('YOUTUBE_CLIENT_SECRET') or os.getenv('YT_CLIENT_SECRET', '')).strip()
    refresh_token = (os.getenv('YOUTUBE_REFRESH_TOKEN') or os.getenv('YT_REFRESH_TOKEN', '')).strip()

    # If env vars not set, attempt loading from local token JSON
    if not all([client_id, client_secret, refresh_token]):
        for p in LOCAL_TOKEN_PATHS:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    client_id = data.get("client_id", "").strip()
                    client_secret = data.get("client_secret", "").strip()
                    refresh_token = data.get("refresh_token", "").strip()
                    if all([client_id, client_secret, refresh_token]):
                        print(f"[youtube] Loaded credentials from local token file.")
                        break
                except Exception:
                    pass

    if not all([client_id, client_secret, refresh_token]):
        print("[youtube] ⚠️ Missing credentials! Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.")
        return None

    def mask(s): return f"{s[:4]}...{s[-4:]}" if s and len(s) > 8 else "SET"
    print(f"[youtube] Client ID: {mask(client_id)}")
    print(f"[youtube] Refresh Token: {mask(refresh_token)}")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube"]
    )

    try:
        creds.refresh(Request())
    except Exception as e:
        print(f"[youtube] ❌ Auth error: {e}")
        return None

    return build('youtube', 'v3', credentials=creds)

def add_video_to_playlist(youtube, video_id, playlist_title=DEFAULT_PLAYLIST_TITLE):
    """Finds or creates the playlist and adds the video to it."""
    try:
        print(f"[youtube] Checking playlists for: '{playlist_title}'...")
        res = youtube.playlists().list(part="snippet", mine=True, maxResults=50).execute()
        playlist_id = None
        for item in res.get("items", []):
            if item["snippet"]["title"].strip().lower() == playlist_title.strip().lower():
                playlist_id = item["id"]
                break

        if not playlist_id:
            print(f"[youtube] Creating new playlist: '{playlist_title}'...")
            new_pl = youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": playlist_title,
                        "description": "Daily Autonomous Pokémon Hardcore Challenge Runs powered by AI minimax battle calculations."
                    },
                    "status": {"privacyStatus": "public"}
                }
            ).execute()
            playlist_id = new_pl["id"]
            import time
            time.sleep(3)

        print(f"[youtube] Adding video {video_id} to playlist {playlist_id}...")
        import time
        for attempt in range(3):
            try:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {"kind": "youtube#video", "videoId": video_id}
                        }
                    }
                ).execute()
                print("[youtube] ✅ Video successfully added to playlist!")
                break
            except Exception as pe:
                if attempt < 2:
                    time.sleep(4)
                else:
                    raise pe
    except Exception as e:
        print(f"[youtube] ⚠️ Playlist notice: {e}")

def upload_to_youtube(video_path, thumbnail_path=None, title=None, description=None, tags=None, playlist_title=DEFAULT_PLAYLIST_TITLE, privacy_status="public"):
    """Full YouTube upload with thumbnail and playlist insertion."""
    print("\n" + "=" * 60)
    print("▶️ YOUTUBE UPLOAD INITIATED (POKÉMON AI CHALLENGE)")
    print("=" * 60)

    youtube = get_authenticated_service()
    if not youtube:
        print("[youtube] ⚠️ Skipping YouTube upload (no valid credentials).")
        return {"status": "skipped", "platform": "youtube"}

    if title is None:
        title = "Can an AI Beat Pokémon with ONLY a Magikarp?! (1 HP Focus Sash Solo Sweep)"

    if tags is None:
        tags = [
            "Pokemon", "Pokemon AI", "Magikarp", "Magikarp Solo Run", 
            "Pokemon Challenge", "Pokemon FireRed", "Focus Sash", "Flail", 
            "Pokemon Champion", "Gaming AI", "AI Plays Pokemon", "Competitive Pokemon"
        ]

    if description is None:
        description = (
            "Can an AI beat Pokémon with ONLY a single Magikarp?\n\n"
            "In this hardcore challenge run, our competitive AI minimax engine pilots a Level 100 Magikarp "
            "against Champion Blue's full Indigo Plateau squad (Pidgeot, Alakazam, Rhydon, Exeggutor, Gyarados, Charizard).\n\n"
            "By abusing Focus Sash endure mechanics and surviving with exactly 1 HP, Magikarp unleashes 200 Base Power Flail "
            "to execute a 100% mathematically calculated solo sweep!\n\n"
            "🔥 Subscribe for daily AI gaming challenges!\n"
            "🎮 Playlist: Pokémon AI Challenge Runs"
        )

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "20" # Gaming
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    print(f"[youtube] Uploading: {title} ({os.path.getsize(video_path) // (1024*1024)} MB)...")

    req = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  -> Upload progress: {int(status.progress() * 100)}%")

    video_id = resp.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"[youtube] ✅ Video published successfully! URL: {video_url}")

    # Upload Custom Thumbnail
    if thumbnail_path and os.path.exists(thumbnail_path):
        print(f"[youtube] Uploading custom thumbnail: {thumbnail_path}...")
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/png")
            ).execute()
            print("[youtube] ✅ Custom thumbnail set successfully!")
        except Exception as e:
            print(f"[youtube] ⚠️ Thumbnail error: {e}")

    # Add to Playlist
    add_video_to_playlist(youtube, video_id, playlist_title)

    return {"status": "success", "platform": "youtube", "video_id": video_id, "url": video_url}

if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    v_path = os.path.join(base_dir, "recordings", "pokemon_magikarp_challenge.mp4")
    t_path = os.path.join(base_dir, "recordings", "thumbnail.png")
    if os.path.exists(v_path):
        upload_to_youtube(v_path, t_path)
    else:
        print(f"[youtube] Video not found at {v_path}. Run generate_pokemon_video.py first.")
