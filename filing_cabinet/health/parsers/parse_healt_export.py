import json
import os
import yaml
from pathlib import Path
from datetime import datetime
from filing_cabinet.health.parsers.runkeeper import parse_runkeeper
from filing_cabinet.health.parsers.sleep import parse_sleep
from filing_cabinet.health.parsers.temp import parse_temperature
from filing_cabinet.health.parsers.hrv import parse_hrv
from filing_cabinet.health.parsers.workout import parse_fitbod

RAW_DIR = Path.home() / "avrana" / "filing_cabinet" / "health" / "raw_exports"
OUT_DIR = Path.home() / "avrana" / "filing_cabinet" / "health"

def load_latest_json():
    files = sorted(RAW_DIR.glob("HealthAutoExport_*.json"), key=os.path.getmtime, reverse=True)
    if not files:
        print("No JSON export files found.")
        return None, None
    latest_file = files[0]
    with open(latest_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return None, None
    date_str = latest_file.stem.split('_')[-2]
    return data, date_str

def main():
    data, date_str = load_latest_json()
    if not data:
        return

    summary = {
        "run": parse_runkeeper(data),
        "sleep": parse_sleep(data),
        "hrv": parse_hrv(data),
        "body_temperature": parse_temperature(data),
        "workout": parse_fitbod(data)
    }

    out_file = OUT_DIR / f"Health_{date_str}.yaml"
    if out_file.exists():
        print(f"{out_file} already exists. Use --force to overwrite.")
        return

    with open(out_file, "w") as f:
        yaml.dump(summary, f, default_flow_style=False)

    print(f"Summary written to {out_file}")

if __name__ == "__main__":
    main()
