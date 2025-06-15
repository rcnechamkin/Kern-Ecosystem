from typing import List, Optional, Dict, Union
from .context_loader import get_codex_context

# === PromptContextBuilder ===
class PromptContextBuilder:
    def __init__(self):
        self.context_modules = get_codex_context()

    def build_prompt(
        self,
        intent_tags: List[str],
        emotional_state: Optional[str] = None,
        weekly_priority: Optional[str] = None
    ) -> str:
        """
        Assembles a full prompt context string using codex modules and intent tags.
        """
        sections = []

        # === Load universal tone and ethics ===
        voice = self.context_modules.get("voice")
        ethics = self.context_modules.get("ethics")

        if voice:
            sections.append(self._format_section("Voice & Tone", voice))
        if ethics:
            sections.append(self._format_section("Ethical Boundaries", ethics))

        # === Include key context by tag ===
        for tag in intent_tags:
            content = self._load_by_tag(tag)
            if content:
                sections.append(self._format_section(tag, content))

        # === Optional emotional state ===
        if emotional_state:
            sections.append(f"\n# Current User Mood\nThe user is feeling: {emotional_state}.\n")

        # === Optional priority ===
        if weekly_priority:
            sections.append(f"\n# Weekly Focus\nPriority this week: {weekly_priority}.\n")

        return "\n".join(sections)

    def _load_by_tag(self, tag: str) -> Union[str, Dict, None]:
        """
        Maps intent tags to context modules. This mapping will evolve over time.
        """
        tag_map = {
            "cbt_support": ["cbt", "identity", "goals"],
            "motivation": ["goals", "identity", "emotional_context"],
            "schedule_check": ["routine", "schedules", "priorities"],
            "reflection": ["journals", "habits", "moods", "week_summaries"],
            "writing_support": ["projects", "media_tastes", "voice"],
        }

        modules = tag_map.get(tag, [])
        result = []

        for module in modules:
            content = self.context_modules.get(module)
            if content:
                result.append(self._format_section(module.title(), content))

        return "\n".join(result) if result else None

    def _format_section(self, title: str, content: Union[str, Dict]) -> str:
        """
        Formats a section of the prompt clearly, adding markdown-style headers.
        """
        if isinstance(content, dict):
            formatted = yaml.safe_dump(content, sort_keys=False)
        else:
            formatted = content.strip()

        return f"\n# {title}\n{formatted}\n"
