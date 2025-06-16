import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
import yaml

# === Setup Project Root ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# === Import Kern Loader and Calendar ===
from filing_cabinet import loader
from kern_calendar.sync import fetch_upcoming_events

# === Constants ===
CATEGORIES = ["journals", "moods", "habits", "cbt", "activity"]
MEDIA_MODULES = {
    "music": "media_sync/music",
    # Future modules: "books": "media_sync/reading", etc.
}
CALENDAR_PATH = Path(PROJECT_ROOT) / "calendar" / "calendar_test.yaml"
OUTPUT_DIR = Path(__file__).resolve().parent

# === Date Range: Previous Monday to Sunday ===
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday() + 7)  # Last Monday
end_of_week = start_of_week + timedelta(days=6)              # Last Sunday

# === Blackbox Data Shell ===
blackbox_data = {
    "week_of": start_of_week.strftime("%Y-%m-%d"),
    "week_range": f"{start_of_week.date()} to {end_of_week.date()}",
    "data": {}
}

# === Load Core Categories ===
for category in CATEGORIES:
    try:
        entries = loader.get_entries_between(category, start_of_week, end_of_week)
        blackbox_data["data"][category] = entries
    except Exception as e:
        print(f"Error loading {category}: {e}")
        blackbox_data["data"][category] = []

# === Load Media Modules (e.g. music logs)
for label, relative_path in MEDIA_MODULES.items():
    full_path = Path(PROJECT_ROOT) / "filing_cabinet" / relative_path
    weekly_entries = []

    if not full_path.exists():
        print(f"Media path not found: {full_path}")
        continue

    for file in full_path.glob("*.yaml"):
        try:
            file_date = datetime.strptime(file.stem, "%Y-%m-%d")
            if start_of_week <= file_date <= end_of_week:
                with open(file, "r") as f:
                    content = yaml.safe_load(f)
                    if content:
                        weekly_entries.append(content)
        except Exception as e:
            print(f"Skipping file {file.name}: {e}")

    blackbox_data["data"][label] = weekly_entries

# === Load Calendar Events ===
try:
    calendar_events = fetch_upcoming_events()
    if calendar_events:
        blackbox_data["upcoming_calendar"] = calendar_events
except Exception as e:
    print(f"Calendar sync failed: {e}")

# === Save Blackbox ===
filename = OUTPUT_DIR / f"blackbox_{start_of_week.strftime('%Y-%m-%d')}.yaml"
with open(filename, "w") as f:
    yaml.dump(blackbox_data, f, default_flow_style=False, allow_unicode=True)

print(f"Blackbox saved to {filename}")
