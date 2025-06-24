# kern_sync/strava/token_refresh.py
import requests, json, datetime
from pathlib import Path

secrets_path = Path("/home/cody/avrana/kern_secrets/strava.json")

def refresh_token():
    creds = json.loads(secrets_path.read_text())
    
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh_token"]
    })

    if response.status_code == 200:
        data = response.json()
        creds["access_token"] = data["access_token"]
        creds["refresh_token"] = data["refresh_token"]
        creds["token_expires_at"] = datetime.datetime.utcfromtimestamp(data["expires_at"]).isoformat() + "Z"
        secrets_path.write_text(json.dumps(creds, indent=2))
        print("Strava token refreshed.")
    else:
        print(f"Failed to refresh token: {response.text}")
