"""
QiyamBreak - Content Loader
Loads and randomly selects duas, tasks, reminders, typing texts.
Validates JSON structure before use. Never crashes on bad data.
"""

import json
import random
from pathlib import Path
from typing import Optional


_CONTENT_DIR = Path(__file__).parent / "content"


def _load_json_safe(filename: str) -> list:
    """Load a JSON file from the content directory. Returns [] on any error."""
    path = _CONTENT_DIR / filename
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.loads(f.read(512_000))  # 500 KB cap
        if not isinstance(data, list):
            return []
        return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def _validate_dua(item: dict) -> bool:
    required = {"arabic", "transliteration", "meaning", "source"}
    return isinstance(item, dict) and required.issubset(item.keys())


def _validate_task(item: dict) -> bool:
    required = {"title", "icon", "instruction", "duration_seconds"}
    return isinstance(item, dict) and required.issubset(item.keys())


def _validate_reminder(item: dict) -> bool:
    required = {"text", "source"}
    return isinstance(item, dict) and required.issubset(item.keys())


def _validate_typing_text(item: dict) -> bool:
    required = {"text", "note"}
    return isinstance(item, dict) and required.issubset(item.keys())


class ContentLoader:
    """
    Lazily loads content JSONs once and caches them.
    Provides random-pick methods for each content type.
    Tracks recently shown items to avoid repetition.
    """

    def __init__(self) -> None:
        self._duas: list = []
        self._tasks: list = []
        self._reminders: list = []
        self._typing_texts: list = []

        # Track last shown IDs to avoid immediate repeats
        self._last_dua_id: Optional[int] = None
        self._last_task_id: Optional[int] = None
        self._last_reminder_id: Optional[int] = None
        self._last_typing_id: Optional[int] = None

        self._loaded = False

    def load(self) -> None:
        """Load all content files. Call once at startup."""
        raw_duas     = _load_json_safe("duas.json")
        raw_tasks    = _load_json_safe("tasks.json")
        raw_reminders = _load_json_safe("reminders.json")
        raw_typing   = _load_json_safe("typing_texts.json")

        self._duas     = [d for d in raw_duas     if _validate_dua(d)]
        self._tasks    = [t for t in raw_tasks    if _validate_task(t)]
        self._reminders = [r for r in raw_reminders if _validate_reminder(r)]
        self._typing_texts = [t for t in raw_typing if _validate_typing_text(t)]

        self._loaded = True

    def _pick(self, items: list, last_id_attr: str) -> Optional[dict]:
        """Pick a random item, avoiding the last-shown one if possible."""
        if not items:
            return None
        last_id = getattr(self, last_id_attr)
        candidates = [i for i in items if i.get("id") != last_id]
        if not candidates:
            candidates = items  # Fallback if only 1 item
        chosen = random.choice(candidates)
        setattr(self, last_id_attr, chosen.get("id"))
        return chosen

    def get_dua(self) -> Optional[dict]:
        return self._pick(self._duas, "_last_dua_id")

    def get_task(self, task_type: Optional[str] = None) -> Optional[dict]:
        """Get a random task. Optionally filter by type (physical/breathing/etc.)."""
        pool = self._tasks
        if task_type:
            filtered = [t for t in self._tasks if t.get("type") == task_type]
            if filtered:
                pool = filtered
        return self._pick(pool, "_last_task_id")

    def get_reminder(self) -> Optional[dict]:
        return self._pick(self._reminders, "_last_reminder_id")

    def get_typing_text(self, category: Optional[str] = None) -> Optional[dict]:
        """Get a random typing text. Optionally filter by category."""
        pool = self._typing_texts
        if category:
            filtered = [t for t in self._typing_texts if t.get("category") == category]
            if filtered:
                pool = filtered
        return self._pick(pool, "_last_typing_id")

    def get_all_duas(self) -> list:
        return list(self._duas)

    def get_all_tasks(self) -> list:
        return list(self._tasks)

    @property
    def is_loaded(self) -> bool:
        return self._loaded


# Module-level singleton
content = ContentLoader()
