from pathlib import Path
import yaml
from typing import List, Dict, Any
from datetime import datetime, date

BASE_PATH = Path(__file__).resolve().parent

def load_yaml_entries(subfolder: str) -> List[Dict[str, Any]]:
    folder_path = BASE_PATH / subfolder
    entries = []
    if not folder_path.exists():
        print(f"[loader.py] Folder does not exist: {folder_path}")
        return entries

    for file in sorted(folder_path.glob("*.yaml")):
        try:
            with open(file, "r") as f:
                data = yaml.safe_load(f)
                entries.append(data)
        except Exception as e:
            print(f"[loader.py] Error reading {file.name}: {e}")
    return entries

def get_latest_entries(subfolder: str, n: int = 5) -> List[Dict[str, Any]]:
    all_entries = load_yaml_entries(subfolder)
    return all_entries[-n:]  # Most recent n entries

def get_entries_between(subfolder: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
    folder_path = BASE_PATH / subfolder
    entries = []
    if not folder_path.exists():
        print(f"[loader.py] Folder does not exist: {folder_path}")
        return entries

    for file in sorted(folder_path.glob("*.yaml")):
        try:
            with open(file, "r") as f:
                data = yaml.safe_load(f)
                entry_date = data.get("date")

                if entry_date:
                    if isinstance(entry_date, str):
                        dt = datetime.strptime(entry_date, "%Y-%m-%d")
                    elif isinstance(entry_date, datetime):
                        dt = entry_date
                    elif isinstance(entry_date, date):
                        dt = datetime.combine(entry_date, datetime.min.time())
                    else:
                        print(f"[loader.py] Unknown date format in file: {file.name}")
                        continue

                    if start <= dt <= end:
                        entries.append(data)
        except Exception as e:
            print(f"[loader.py] Error parsing {file.name}: {e}")
    return entries
