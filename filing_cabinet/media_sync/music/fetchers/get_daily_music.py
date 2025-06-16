import os
import requests
import yaml
from datetime import datetime, timedelta
from dotenv import load_dotenv

# === Load API Key from .env ===
load_dotenv(os.path.expanduser("~/avrana/.env"))
API_KEY = os.getenv("LASTFM_API_KEY")
USERNAME = "rcnechamkin"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# === File Paths ===
TODAY = datetime.now().strftime("%Y-%m-%d")
OUT_DIR = os.path.expanduser("~/avrana/filing_cabinet/media_sync/music")
OUT_PATH = os.path.join(OUT_DIR, f"Music_{TODAY}.yaml")

# === Create directory if it doesn't exist ===
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_tracks():
    params = {
        "method": "user.getrecenttracks",
        "user": USERNAME,
        "api_key": API_KEY,
        "format": "json",
        "limit": 200,
        "from": int((datetime.now() - timedelta(hours=24)).timestamp()),
        "to": int(datetime.now().timestamp())
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    tracks = data.get("recenttracks", {}).get("track", [])

    parsed = []
    for t in tracks:
        if not t.get("date"): continue  # skip 'Now Playing'

        parsed.append({
            "artist": t["artist"]["#text"],
            "track": t["name"],
            "album": t.get("album", {}).get("#text", ""),
            "played_at": t["date"]["#text"]
        })
    return parsed

def deduplicate(existing, new):
    seen = set()
    combined = existing + new
    result = []
    for t in combined:
        key = (t["artist"], t["track"], t["played_at"])
        if key not in seen:
            seen.add(key)
            result.append(t)
    return sorted(result, key=lambda x: x["played_at"])

def load_existing():
    if not os.path.exists(OUT_PATH):
        return []
    with open(OUT_PATH, "r") as f:
        return yaml.safe_load(f) or []

def save_data(tracks):
    with open(OUT_PATH, "w") as f:
        yaml.dump(tracks, f, sort_keys=False, allow_unicode=True)
    print(f"Saved {len(tracks)} unique tracks to {OUT_PATH}")

if __name__ == "__main__":
    try:
        existing = load_existing()
        new_tracks = fetch_tracks()
        all_tracks = deduplicate(existing, new_tracks)
        save_data(all_tracks)
    except Exception as e:
        print(f"Error: {e}")
