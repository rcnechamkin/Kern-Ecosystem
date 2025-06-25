import yaml
from pathlib import Path
from datetime import datetime
import spacy

# === Load spaCy model ===
nlp = spacy.load("en_core_web_sm")

# === Project paths ===
FILING = Path.home() / "avrana" / "filing_cabinet"
CORE = FILING / "core"

# === WordNet synonym expansion (via local synonym_expander.py) ===
from synonym_expander import expand_tags

# === INTENT TAG INFERENCE ===

def extract_keywords_spacy(text, min_len=3):
    """Extract base keywords from user prompt using spaCy noun/adjective tokens."""
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if (
            not token.is_stop and
            not token.is_punct and
            token.pos_ in {"NOUN", "ADJ"} and
            len(token.text) >= min_len
        ):
            keywords.add(token.lemma_.lower())

    return sorted(keywords)

def infer_intent_tags_from_prompt(prompt_text: str) -> list:
    """Returns expanded, deduplicated list of smart tags for use in Codex routing."""
    base = extract_keywords_spacy(prompt_text)
    expanded = expand_tags(base)
    return sorted(set(expanded))

# === RECENT MEMORY CONTEXT ===

def load_latest_yaml_entries(folder: str, count: int = 3, pattern: str = "*.yaml") -> list:
    """Load most recent YAML files from a given memory folder."""
    p = FILING / folder
    if not p.exists():
        return []

    files = sorted(p.glob(pattern), reverse=True)
    entries = []
    for f in files[:count]:
        try:
            data = yaml.safe_load(f.open())
            if data:
                entries.append(data)
        except Exception as e:
            print(f"[!] Failed to load {f.name}: {e}")
    return entries

def load_recent_context() -> dict:
    """Returns a dictionary of recent logs for use in GPT prompt assembly."""
    return {
        "recent_runs": load_latest_yaml_entries("runs", count=2),
        "recent_sleep": load_latest_yaml_entries("health", count=2),
        "recent_music": load_latest_yaml_entries("media_sync/music", count=2),
        "recent_journals": load_latest_yaml_entries("journals", count=2),
    }

# === DEBUGGING ===

if __name__ == "__main__":
    prompt = input("Enter prompt for tag inference:\n> ")
    tags = infer_intent_tags_from_prompt(prompt)
    print(f"\n[✓] Inferred tags: {tags}")

    recent = load_recent_context()
    print(f"\n[✓] Loaded recent entries:")
    for k, v in recent.items():
        print(f"  {k}: {len(v)} files")
