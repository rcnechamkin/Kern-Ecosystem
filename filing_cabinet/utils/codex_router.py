import yaml
from datetime import datetime
from pathlib import Path
from codex_utils import infer_intent_tags_from_prompt
from synonym_expander import expand_tags

TAG_INDEX_PATH = Path.home() / "avrana" / "filing_cabinet" / "core" / "tag_index.yaml"
MAX_FILES = 5

def load_tag_index():
    try:
        with open(TAG_INDEX_PATH, "r") as f:
            return yaml.safe_load(f).get("tags", {})
    except Exception as e:
        print(f"[!] Failed to load tag_index.yaml: {e}")
        return {}

def score_files_by_tags(expanded_tags):
    tag_index = load_tag_index()
    file_scores = {}

    for tag in expanded_tags:
        tag_data = tag_index.get(tag)
        if not tag_data:
            continue

        for file in tag_data.get("files", []):
            score = file_scores.get(file, 0)
            file_scores[file] = score + 1  # 1 point per matching tag

    sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    return [f for f, _ in sorted_files[:MAX_FILES]]

def get_relevant_files(prompt_text=None, intent_tags=None):
    if not intent_tags and not prompt_text:
        print("[!] Must provide either `intent_tags` or `prompt_text`.")
        return []

    if not intent_tags:
        print(f"[🧠] Inferring tags from prompt: {prompt_text}")
        intent_tags = infer_intent_tags_from_prompt(prompt_text)

    print(f"[→] Final intent tags: {intent_tags}")
    all_tags = expand_tags(intent_tags)

    print(f"[→] Expanded tags: {all_tags}")
    return score_files_by_tags(all_tags)

# === CLI for testing ===

if __name__ == "__main__":
    print("== Codex Router: Smart Memory Retrieval ==")
    raw = input("Enter a question or keywords:\n> ").strip()

    if "," in raw:
        tags = [x.strip().lower() for x in raw.split(",")]
        result = get_relevant_files(intent_tags=tags)
    else:
        result = get_relevant_files(prompt_text=raw)

    print("\n[✓] Relevant files:")
    for f in result:
        print(f"  - {f}")
