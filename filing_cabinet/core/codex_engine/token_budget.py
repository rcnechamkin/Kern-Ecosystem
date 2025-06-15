from typing import Dict, List, Tuple, Union
from . import nlp_filters

MAX_TOKENS = 4096
TOKEN_BUFFER = 512  # reserve space for user input + system prompt
MAX_CONTEXT_TOKENS = MAX_TOKENS - TOKEN_BUFFER
CHARS_PER_TOKEN = 3.5


def estimate_tokens(text: str) -> int:
    """Rough token estimate using avg chars/token for English (≈3.5)."""
    return int(len(text) / CHARS_PER_TOKEN)


def truncate_to_token_limit(sections: List[Tuple[str, Union[str, Dict]]], max_tokens: int = MAX_CONTEXT_TOKENS) -> str:
    """
    Truncates or compresses prompt sections to fit within token budget.
    Each section is a (title, content) tuple.
    """
    output = []
    used_tokens = 0

    for title, content in sections:
        formatted = format_section(title, content)
        section_tokens = estimate_tokens(formatted)

        if used_tokens + section_tokens > max_tokens:
            # Try summarizing if it's a dict
            if isinstance(content, dict):
                compressed = nlp_filters.summarize_dict(content, max_keys=3)
                compressed_formatted = format_section(title + " (summary)", compressed)
                compressed_tokens = estimate_tokens(compressed_formatted)

                if used_tokens + compressed_tokens <= max_tokens:
                    output.append(compressed_formatted)
                    used_tokens += compressed_tokens
                else:
                    continue  # skip if still too long
            else:
                continue  # skip long markdown sections
        else:
            output.append(formatted)
            used_tokens += section_tokens

    return "\n".join(output)


def format_section(title: str, content: Union[str, Dict]) -> str:
    if isinstance(content, dict):
        return f"\n# {title}\n" + nlp_filters.flatten_dict_to_bullets(content)
    elif isinstance(content, str):
        return f"\n# {title}\n{content.strip()}"
    else:
        return f"\n# {title}\n{str(content)}"
