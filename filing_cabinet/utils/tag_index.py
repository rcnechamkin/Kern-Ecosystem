import yaml
from pathlib import Path
from datetime import datetime

# === Config ===
FILING_CABINET = Path.home() / "avrana" / "filing_cabinet"
TARGET_FOLDERS = ["journals", "cbt", "week_summaries"]
INDEX_OUTPUT = FILING_CABINET / "core" / "tag_index.yaml"

def parse_date_from_filename(filename):
    try:
        return datetime.strptime(filename.stem, "%Y-%m-%d").date()
    except:
        return None

def collect_tags():
    tag_index = {}

    for folder_name in TARGET_FOLDERS:
        folder = FILING_CABINET / folder_name
        if not folder.exists():
            continue

        for file in folder.glob("*.yaml"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                print(f"[!] Skipping {file.name}: YAML load error")
                continue

            tags = data.get("tags", [])
            if not tags:
                continue

            date = parse_date_from_filename(file)
            for tag in tags:
                if tag not in tag_index:
                    tag_index[tag] = {
                        "count": 1,
                        "last_seen": str(date) if date else None,
                        "files": [str(file.relative_to(FILING_CABINET))]
                    }
                else:
                    tag_index[tag]["count"] += 1
                    tag_index[tag]["files"].append(str(file.relative_to(FILING_CABINET)))

                    # Update last seen if newer
                    if date:
                        last = tag_index[tag].get("last_seen")
                        if not last or date > datetime.fromisoformat(last).date():
                            tag_index[tag]["last_seen"] = str(date)

    # Sort and return as normal dict
    sorted_tags = dict(sorted(tag_index.items(), key=lambda x: x[1]["count"], reverse=True))
    return {"tags": sorted_tags}

def save_index(index_data):
    with open(INDEX_OUTPUT, "w", encoding="utf-8") as f:
        yaml.dump(index_data, f, sort_keys=False, allow_unicode=True)
    print(f"[✓] Tag index saved to: {INDEX_OUTPUT}")

if __name__ == "__main__":
    tag_data = collect_tags()
    save_index(tag_data)
