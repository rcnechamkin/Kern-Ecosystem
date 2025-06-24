import requests, json
from pathlib import Path

code = "3022d25e3063dab97081232a62fb23b884ae6215"
client_id = "165690"
client_secret = "7c98b5446c563f960776a4a7d6ce9fad079065ff"
secrets_path = Path("/home/cody/avrana/kern_secrets/strava.json")

resp = requests.post("https://www.strava.com/api/v3/oauth/token", data={
    "client_id": client_id,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code"
})

if resp.status_code == 200:
    data = resp.json()
    secrets_path.write_text(json.dumps({
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_expires_at": data["expires_at"]
    }, indent=2))
    print("✅ Tokens saved.")
else:
    print(f"❌ Error: {resp.status_code} - {resp.text}")
