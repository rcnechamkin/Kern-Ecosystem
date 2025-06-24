from datetime import datetime

def parse_apple_workouts(data):
    try:
        workouts = data["data"].get("workouts", [])
    except (KeyError, TypeError):
        return {"error": "Invalid data format: 'workouts' section missing"}

    # Filter for run-type workouts with valid data
    runs = []
    for w in workouts:
        if w.get("name", "").lower() == "run" and w.get("distance") and w.get("start") and w.get("end"):
            try:
                start = datetime.strptime(w["start"], "%Y-%m-%d %H:%M:%S %z")
                end = datetime.strptime(w["end"], "%Y-%m-%d %H:%M:%S %z")
                duration = (end - start).total_seconds() / 60
                distance = float(w["distance"]["qty"])
                if duration > 5 and distance > 0.5:
                    runs.append({
                        "timestamp": start,
                        "duration": duration,
                        "distance": distance,
                        "energy": float(w.get("activeEnergyBurned", {}).get("qty", 0.0))
                    })
            except Exception:
                continue

    if not runs:
        return {"note": "No valid Apple Health runs found."}

    latest = max(runs, key=lambda x: x["timestamp"])
    pace = round(latest["duration"] / latest["distance"], 2) if latest["distance"] else None

    return {
        "date": latest["timestamp"].strftime("%Y-%m-%d"),
        "source": "Apple Health (workouts)",
        "duration_minutes": round(latest["duration"], 1),
        "distance_mi": round(latest["distance"], 2),
        "avg_pace_min_per_mi": pace
    }
