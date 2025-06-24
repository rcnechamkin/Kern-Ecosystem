import sys
from pathlib import Path
import yaml
from datetime import datetime
import argparse
from openai import OpenAI

# === Add project root to sys.path ===
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.env import get_openai_key

# === Config ===
MODEL = "gpt-4o-mini"
FILING_CABINET = ROOT / "filing_cabinet"
SKIP_FOLDERS = {"core", "archive"}
TAG_FIELDS = ["tags", "summary", "emotion"]

client = OpenAI(api_key=get_openai_key())

def get_all_tag_folders() -> list:
    folders = []

    for p in FILING_CABINET.iterdir():
        if p.name in SKIP_FOLDERS or not p.is_dir():
            continue
        folders.append(p)

        # Special handling for nested folders like media_sync
        if p.name == "media_sync":
            nested = p / "music"
            if nested.exists():
                folders.append(nested)

    return folders


def get_files_to_tag(folder: Path, retag: bool = False) -> list:
    return [
        f for f in folder.glob("*.yaml")
        if retag or "kern_generated" not in open(f, encoding="utf-8").read()
    ]

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(path: Path, data: dict):
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def clean_gpt_output(content: str) -> str:
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1].strip()
    return content

def generate_tags(content_text: str) -> dict:
    prompt = f"""You are Kern, an emotionally aware but sardonic assistant who is looking at Cody's data.
Given the following memory entry, return a valid YAML block with:
- tags: 3–5 lowercase keywords that describe tone, genre for media, and context (e.g. ambient, grief, focus, punk, roadtrip)
- summary: 1–2 sentence summary
- emotion: a single emotional word (optional if not present in text)

Only return raw YAML. No code blocks, no formatting.

Memory Entry:
\"\"\"
{content_text.strip()}
\"\"\"
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content
    try:
        clean = clean_gpt_output(content)
        return yaml.safe_load(clean)
    except Exception as e:
        print(f"[ERROR] YAML parse failed:\n{e}\n---\n{content}")
        return {}

def apply_airik_metadata(fields: dict, model: str = MODEL) -> dict:
    now = datetime.utcnow().isoformat()
    return {
        field: {
            "by": "kern",
            "model": model,
            "created": now
        } for field in fields.keys()
    }

def tag_folder(folder: Path, dry_run: bool, retag: bool):
    print(f"\nTagging: {folder.name}/")
    files = get_files_to_tag(folder, retag)
    print(f"  [INFO] {len(files)} untagged or retaggable files")

    for file in files:
        print(f"    ↪ {file.name}")
        data = load_yaml(file)
        content_text = yaml.safe_dump(data)

        tags = generate_tags(content_text)
        if not tags:
            print(f"    [!] Skipped: Error parsing tags")
            continue

        if dry_run:
            print(f"\n--- Preview for {file.name} ---\n{yaml.safe_dump(tags)}\n")
        else:
            data.update(tags)
            data["kern_generated"] = apply_airik_metadata(tags)
            save_yaml(file, data)
            print(f"    [✓] Tagged and saved with AIRIK attribution")

def main():
    parser = argparse.ArgumentParser(description="Smart AIRIK-compliant tagger for all memory folders.")
    parser.add_argument("--dry", action="store_true", help="Preview tags without saving")
    parser.add_argument("--retag", action="store_true", help="Force overwrite existing tags")
    args = parser.parse_args()

    folders = get_all_tag_folders()
    for folder in folders:
        tag_folder(folder, dry_run=args.dry, retag=args.retag)

if __name__ == "__main__":
    main()
