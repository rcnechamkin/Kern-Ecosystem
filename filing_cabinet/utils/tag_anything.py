import yaml
from pathlib import Path
from openai import OpenAI
from datetime import datetime
import argparse

# === OpenAI setup ===
client = OpenAI()
MODEL = "gpt-4o-mini"
TAG_FIELDS = ["tags", "summary", "emotion"]

def get_files_to_tag(target_dir: Path) -> list:
    return [
        f for f in target_dir.glob("*.yaml")
        if not any(tag in open(f, encoding="utf-8").read() for tag in TAG_FIELDS)
    ]

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(path: Path, data: dict):
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def generate_tags(content_text: str) -> dict:
    prompt = f"""You are Kern, a sharp but emotionally aware assistant.
Analyze the following YAML-style memory entry and return a valid YAML block with:
- tags: 3–5 lowercase keywords
- summary: 1–2 sentence summary
- emotion: (optional) one-word emotional tone, only if emotional content is present

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
    output = response.choices[0].message.content
    try:
        return yaml.safe_load(output)
    except Exception as e:
        print(f"[ERROR] Failed to parse YAML from GPT: {e}\n---\n{output}")
        return {}

def apply_airik_compliance(generated_fields: dict, model: str = MODEL) -> dict:
    now = datetime.utcnow().isoformat()
    return {
        field: {
            "by": "kern",
            "model": model,
            "created": now
        } for field in generated_fields.keys()
    }

def process_directory(folder: str, dry_run: bool = False):
    target_dir = Path(f"filing_cabinet/{folder}/")
    if not target_dir.exists():
        print(f"[ERROR] Folder not found: {target_dir}")
        return

    files = get_files_to_tag(target_dir)
    print(f"[INFO] Found {len(files)} untagged entries in {folder}/")

    for file in files:
        print(f"[→] Tagging: {file.name}")
        data = load_yaml(file)
        content_text = yaml.safe_dump(data)

        tags = generate_tags(content_text)
        if not tags:
            print(f"[!] Skipped {file.name} due to tagging error.")
            continue

        if dry_run:
            print(f"\n--- Suggested Tags for {file.name} ---\n{yaml.safe_dump(tags)}\n")
        else:
            data.update(tags)
            data["kern_generated"] = apply_airik_compliance(tags)
            save_yaml(file, data)
            print(f"[✓] Updated {file.name} with AIRIK-compliant tags.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart tagger for any memory directory.")
    parser.add_argument("folder", help="Folder inside filing_cabinet/ (e.g., moods, habits, gratitude)")
    parser.add_argument("--dry", action="store_true", help="Preview tagging without saving")
    args = parser.parse_args()

    process_directory(folder=args.folder, dry_run=args.dry)
