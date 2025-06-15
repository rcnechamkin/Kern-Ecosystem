import yaml
from typing import Union, Dict, List

# === Rule-Based Summarization and Filters ===

def extract_relevant_fields(
    content: Union[Dict, str],
    keywords: List[str],
    max_entries: int = 3
) -> Union[str, Dict]:
    """
    Filters YAML/dict-style content to only include entries that match keywords.
    For example: filter journal entries with 'burnout', 'discipline', etc.
    """
    if isinstance(content, str):
        # For markdown: do keyword filter on paragraph chunks
        return _filter_markdown_by_keywords(content, keywords, max_entries)

    if isinstance(content, dict):
        return _filter_dict_by_keywords(content, keywords, max_entries)

    return content


def _filter_dict_by_keywords(data: Dict, keywords: List[str], max_entries: int) -> Dict:
    """
    Returns filtered dictionary entries where any keyword appears in the value (case-insensitive).
    """
    filtered = {}
    count = 0
    for key, value in reversed(list(data.items())):  # assume later entries are newer
        if count >= max_entries:
            break

        value_str = yaml.safe_dump(value) if isinstance(value, dict) else str(value)
        if any(kw.lower() in value_str.lower() for kw in keywords):
            filtered[key] = value
            count += 1

    return filtered


def _filter_markdown_by_keywords(text: str, keywords: List[str], max_chunks: int) -> str:
    """
    Naive keyword-based markdown filter. Returns up to max_chunks matching paragraphs.
    """
    chunks = text.strip().split("\n\n")
    results = []

    for chunk in chunks:
        if any(kw.lower() in chunk.lower() for kw in keywords):
            results.append(chunk.strip())
            if len(results) >= max_chunks:
                break

    return "\n\n".join(results)


def summarize_dict(data: Dict, max_keys: int = 5)
