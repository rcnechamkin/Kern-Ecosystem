from datetime import datetime, timedelta
from pathlib import Path
import sys
import yaml

#Make sure project root is on sys.path BEFORE importing loader
sys.path.append(str(Path(__file__).resolve().parent.parent))

#Import loader AFTER the path is fixed
from filing_cabinet import loader

# Optional: debug the path if needed
# print("🧭 PYTHON PATH:")
# for p in sys.path:
#     print("  -", p)

#Define time range: previous Monday to Sunday
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday() + 7)  # Last Monday
end_of_week = start_of_week + timedelta(days=6)              # Last Sunday

#Subfolders to extract
categories = ["journals", "moods", "habits", "cbt", "activity"]

#Collect data
blackbox_data = {
    "week_of": start_of_week.strftime("%Y-%m-%d"),
    "week_range": f"{start_of_week.date()} to {end_of_week.date()}",
    "data": {}
}

for category in categories:
    entries = loader.get_entries_between(category, start_of_week, end_of_week)
    blackbox_data["data"][category] = entries

#Save to file
output_dir = Path(__file__).resolve().parent
filename = output_dir / f"blackbox_{start_of_week.strftime('%Y-%m-%d')}.yaml"

with open(filename, "w") as f:
    yaml.dump(blackbox_data, f, default_flow_style=False)

print(f"✅ Black box saved to {filename}")
