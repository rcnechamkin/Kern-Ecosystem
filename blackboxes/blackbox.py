import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

print("🧭 PYTHON PATH:")
for p in sys.path:
    print("  -", p)
from kern_calendar.sync import fetch_upcoming_events
import yaml

# Add project root to sys.path BEFORE importing loader
sys.path.append("/home/cody/avrana")
print("🧭 PYTHON PATH:")
for p in sys.path:
    print("  -", p)


# Import loader AFTER sys.path is updated
from filing_cabinet import loader

# === Constants ===
CATEGORIES = ["journals", "moods", "habits", "cbt", "activity"]
CALENDAR_PATH = Path(__file__).resolve().parent.parent / "calendar" / "calendar_test.yaml"
OUTPUT_DIR = Path(__file__).resolve().parent

# === Date Range: Previous Monday to Sunday ===
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday() + 7)  # Last Monday
end_of_week = start_of_week + timedelta(days=6)              # Last Sunday

# === Load Memory Logs ===
blackbox_data = {
    "week_of": start_of_week.strftime("%Y-%m-%d"),
    "week_range": f"{start_of_week.date()} to {end_of_week.date()}",
    "data": {}
}

for category in CATEGORIES:
    entries = loader.get_entries_between(category, start_of_week, end_of_week)
    blackbox_data["data"][category] = entries

# === Load Future Calendar Events (if present) ===
calendar_events = fetch_upcoming_events() #Google Calendar Sync
if calendar_events:
    blackbox_data["upcoming_calendar"] = calendar_events

# === Save Blackbox ===
filename = OUTPUT_DIR / f"blackbox_{start_of_week.strftime('%Y-%m-%d')}.yaml"
with open(filename, "w") as f:
    yaml.dump(blackbox_data, f, default_flow_style=False)

print(f"Black box saved to {filename}")
