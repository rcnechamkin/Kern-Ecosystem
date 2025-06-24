import sys
import os
import yaml
import argparse
from pathlib import Path
SysPath = Path

KERN_ROOT = SysPath.home() / "avrana"
if str(KERN_ROOT) not in sys.path:
    sys.path.insert(0, str(KERN_ROOT))

from datetime import datetime, timezone
from openai import OpenAI
from dotenv import load_dotenv
from core.airik_enforcer import load_airik_manifesto

# === Load environment variables ===
load_dotenv(os.path.expanduser("~/avrana/.env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

# === Paths ===
MUSIC_DIR = Path.home() / "avrana" / "filing_cabinet" / "media_sync" / "music"
PROFILE_PATH = Path.home() / "avrana" / "filing_cabinet" / "core" / "media_profile.yaml"

def get_latest_music_file():
    files = sorted(MUSIC_DIR.glob("Music_*.yaml"), reverse=True)
    return files[0] if files else None

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True, Dumper=NoAliasDumper)

def clean_gpt_output(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        return parts[1].strip() if len(parts) > 1 else text
    return text

def build_prompt(summary, top_artists, nostalgic_artists, tracks):
    return f"""You are Kern, an emotionally intelligent assistant tasked with summarizing Cody's music listening for today.
You are creating a YAML block called `kern_summary` for inclusion in a memory file.
Do not wrap your response in code blocks. No triple backticks.

Consider:
- Emotional tone of today's listening
- Overlap with Cody's nostalgic artists: {', '.join(nostalgic_artists)}
- **Why** Cody listened: writing, running/working out, recovery, new releases, artist exploration, etc.
- Whether nostalgic artists released **new work** (this changes intent)
- Don’t assume nostalgia just because the artist is familiar—look at the tracks
- Musical variety and mood
- Eclecticism is OK—interpret it!

Respond ONLY with a raw YAML block called kern_summary containing:
  purpose: why Cody likely listened (e.g. emotional reset, writing, nostalgia loop)
  emotions: list of 2–3 core emotional tones
  tone_profile: genre/style blend, with approximate weights (e.g. ambient: 40%)
  summary: 1–2 sentence reflective analysis of Cody’s listening today
  tags: YAML list of 3–6 lowercase descriptors (e.g. - writing-mode, - ambient, - grief, - punk)
  kern_generated: AIRIK metadata block

You may base your response on:
Summary: {summary}
Top Artists: {top_artists}
Tracks:
{yaml.safe_dump(tracks, allow_unicode=True)}
"""

def run(dry=False):
    music_path = get_latest_music_file()
    if not music_path:
        print("No daily music file found.")
        return

    music_data = load_yaml(music_path)
    if isinstance(music_data, list):
        music_data = {"tracks": music_data}

    profile_data = load_yaml(PROFILE_PATH)
    top_artists_profile = set(profile_data.get("top_artists", []))
    weekly_artists = {t["artist"] for t in music_data.get("tracks", [])}
    nostalgic_artists = sorted(weekly_artists & top_artists_profile)

    prompt = build_prompt(
        summary=music_data.get("summary", ""),
        top_artists=music_data.get("top_artists", []),
        nostalgic_artists=nostalgic_artists,
        tracks=music_data.get("tracks", []),
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    raw_output = response.choices[0].message.content.strip()
    cleaned_output = clean_gpt_output(raw_output)

    try:
        summary_block = yaml.safe_load(cleaned_output)
    except Exception as e:
        print(f"YAML parse error: {e}\n\nRaw output:\n{raw_output}")
        return

    # Attach AIRIK metadata block
    airik = load_airik_manifesto()
    summary_block["kern_summary"]["kern_generated"] = {
        "by": "kern",
        "model": MODEL,
        "airik_enforced": True,
        "created": datetime.now(timezone.utc).isoformat()
    }

    music_data.update(summary_block)

    if dry:
        print("\n--- DRY RUN ---\n")
        print(yaml.safe_dump(music_data.get("kern_summary", {}), sort_keys=False))
    else:
        save_yaml(music_path, music_data)
        print(f"Summary saved to {music_path.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize today's Last.fm music logs with emotional tone and intent.")
    parser.add_argument("--dry", action="store_true", help="Print summary without saving")
    args = parser.parse_args()
    run(dry=args.dry)
