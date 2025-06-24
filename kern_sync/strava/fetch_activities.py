# kern_sync/strava/fetch_activities.py
import requests, json, yaml
from pathlib import Path
from datetime import datetime
from token_refresh import refresh_token

SECRETS_PATH = Path("/home/cody/avrana/kern_secrets/strava.json")
LOG_PATH = Path("/home/cody/avrana/filing_cabinet/health/workouts")

def get_access_token():
    creds = json.loads(SECRETS_PATH.read_text())
    return creds["access_token"]

def fetch_recent_activities():
    refresh_token()  # ensure fresh token
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers=headers,
        params={"per_page": 10}
    )
    
    if response.status_code != 200:
        print(f"Failed to fetch activities: {response.text}")
        return []
    
    return response.json()

def filter_fitbod_activities(activities):
    return [
        act for act in activities
        if act.get("type") in ["Workout", "WeightTraining"] or "fitbod" in (act.get("description") or "").lower()
    ]

def log_activity_to_yaml(activity):
    dt = datetime.fromisoformat(activity["start_date_local"])
    fname = LOG_PATH / f"Fitbod_{dt.date()}.yaml"
    data = {
        "date": dt.date().isoformat(),
        "source": "strava_fitbod",
        "name": activity["name"],
        "duration_minutes": round(activity["elapsed_time"] / 60, 2),
        "notes": activity.get("description", "").strip(),
        "tags": ["fitbod", "strength"]
    }
    
    fname.parent.mkdir(parents=True, exist_ok=True)
    with open(fname, "w") as f:
        yaml.dump(data, f)
    print(f"Logged Fitbod workout to {fname}")

def main():
    acts = fetch_recent_activities()
    fitbod = filter_fitbod_activities(acts)
    
    if not fitbod:
        print("No Fitbod workouts found.")
        return
    
    for act in fitbod:
        log_activity_to_yaml(act)

if __name__ == "__main__":
    main()
