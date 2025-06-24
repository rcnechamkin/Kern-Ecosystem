from datetime import datetime, timedelta

def parse_runkeeper(data):
    try:
        records = data["metrics"]
    except KeyError:
        return {"run": {"error": "Invalid data format: 'metrics' section missing"}}

    entries = []
    for rec in records:
        # Only include valid Runkeeper entries with distance data
        if (
            rec.get("source", "").endswith("Runkeeper") and
            "qty" in rec and
            "date" in rec and
            rec.get("unit") in ["km", "mi"]
        ):
            try:
                timestamp = datetime.strptime(rec["date"], "%Y-%m-%d %H:%M:%S %z")
                distance_km = float(rec["qty"])
                if rec["unit"] == "mi":
                    distance_km *= 1.60934  # Convert miles to kilometers
                entries.append({
                    "timestamp": timestamp,
                    "distance_km": distance_km
                })
            except Exception:
                continue

    if not entries:
        return {"run": {"note": "No Runkeeper entries found."}}

    entries.sort(key=lambda x: x["timestamp"])

    # Group into sessions (<= 5 minutes between data points)
    grouped = []
    current_group = [entries[0]]
    for i in range(1, len(entries)):
        delta = entries[i]["timestamp"] - entries[i-1]["timestamp"]
        if delta <= timedelta(minutes=5):
            current_group.append(entries[i])
        else:
            grouped.append(current_group)
            current_group = [entries[i]]
    grouped.append(current_group)

    # Select the longest run session
    best_run = max(grouped, key=lambda g: len(g))
    total_distance_km = round(sum(e["distance_km"] for e in best_run), 2)
    total_minutes = round((best_run[-1]["timestamp"] - best_run[0]["timestamp"]).total_seconds() / 60, 2)
    pace = round(total_minutes / total_distance_km, 2) if total_distance_km else None

    return {
        "run": {
            "date": best_run[0]["timestamp"].strftime("%Y-%m-%d"),
            "source": "Runkeeper",
            "duration_minutes": total_minutes,
            "distance_km": total_distance_km,
            "avg_pace_min_per_km": pace
        }
    }
