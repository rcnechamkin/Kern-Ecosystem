from core.airik_enforcer import load_airik_manifesto, verify_signature
from pathlib import Path
import openai
from core.env import get_openai_key

openai.api_key = get_openai_key()


VOICE_PATH = Path("filing_cabinet/core/kern_voice.md")


def load_airik_as_string() -> str:
    data = load_airik_manifesto()["airik_manifesto"]
    output = f"AIRIK Manifest v{data['version']} (Enforced)\n"
    output += f"Author: {data['author']} | Updated: {data['updated']}\n"
    output += f"Prime Directive:\n{data['prime_directive'].strip()}\n\n"

    for section, contents in data.items():
        if section in ("version", "issued", "updated", "author", "override_phrase", "prime_directive", "creator_signature"):
            continue
        title = section.replace("_", " ").title()
        output += f"{title}:\n"
        if isinstance(contents, dict):
            for k, v in contents.items():
                output += f"- {k.replace('_', ' ').title()}: {v.strip() if isinstance(v, str) else v}\n"
        elif isinstance(contents, list):
            for item in contents:
                output += f"- {item.strip() if isinstance(item, str) else item}\n"
        output += "\n"
    return output.strip()


def load_kern_personality() -> str:
    if not VOICE_PATH.exists():
        return "Respond in a dry, sardonic tone. Be intelligent, blunt, and never earnest."
    return VOICE_PATH.read_text().strip()


def kern_chat(intent: str, user_input: str, model="gpt-3.5-turbo", temperature=0.7):
    """Builds OpenAI-style messages, injects AIRIK and Kern tone, and sends chat request."""
    verify_signature()

    airik_prompt = load_airik_as_string()
    kern_voice = load_kern_personality()

    messages = [
        {"role": "system", "content": airik_prompt},
        {"role": "system", "content": kern_voice},
        {"role": "user", "content": f"[Intent: {intent}]\n{user_input}"}
    ]

    return openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
