"""
QiyamBreak - Configuration Manager
Handles all user settings with strict validation.
Security: JSON only (no pickle), type-checked, range-clamped.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any


# ── Config schema: field → (type, min, max, default) ──────────────────────────
_SCHEMA: dict[str, tuple] = {
    "sit_minutes":          (int,   5,   180,  30),
    "break_seconds":        (int,   30,  300,  120),
    "theme":                (str,   None, None, "fajr_dawn"),
    "random_theme":         (bool,  None, None, False),
    "show_games":           (bool,  None, None, True),
    "show_duas":            (bool,  None, None, True),
    "show_tasks":           (bool,  None, None, True),
    "typing_mode":          (str,   None, None, "accuracy"),  # "accuracy" or "timed"
    "sound_enabled":        (bool,  None, None, True),
    "start_on_boot":        (bool,  None, None, False),
    "language":             (str,   None, None, "en"),
    "game_rotation":        (list,  None, None, ["typing", "reflex", "math",
                                                  "breathing", "memory", "posture"]),
    "first_run":            (bool,  None, None, True),
    "total_breaks_taken":   (int,   0,    999999, 0),
    "typing_best_wpm":      (float, 0.0,  300.0,  0.0),
    "typing_best_accuracy": (float, 0.0,  100.0,  0.0),
}

_VALID_THEMES = [
    "fajr_dawn", "night_qadr", "desert_sand", "al_andalus", "layl",
    "noor", "forest_dhikr", "madina_blue", "amber_terminal",
    "kufic_geometry", "olive_gold", "storm_urgency", "sakura", "random"
]

_VALID_TYPING_MODES = ["accuracy", "timed"]
_VALID_LANGUAGES    = ["en"]
_VALID_GAMES        = ["typing", "reflex", "math", "breathing", "memory", "posture"]


def _get_config_path() -> Path:
    """Return platform-appropriate config file path."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home() / ".config"
    config_dir = base / "QiyamBreak"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def _sanitize_string(value: str, max_len: int = 64) -> str:
    """Strip control characters and limit length. Prevents injection via config."""
    if not isinstance(value, str):
        return ""
    # Allow only printable ASCII + underscore (theme IDs, etc.)
    cleaned = "".join(c for c in value if c.isprintable())
    return cleaned[:max_len].strip()


def _validate_field(key: str, value: Any) -> Any:
    """
    Validate and sanitize a single config field.
    Returns the sanitized value or the schema default on failure.
    Never raises — always returns a safe value.
    """
    if key not in _SCHEMA:
        return None  # Unknown key — discard silently

    expected_type, min_val, max_val, default = _SCHEMA[key]

    # ── Type coercion ──────────────────────────────────────────────────────────
    try:
        if expected_type == bool:
            # bool check must come before int (bool is a subclass of int in Python)
            if not isinstance(value, bool):
                return default
        elif expected_type == int:
            value = int(value)
        elif expected_type == float:
            value = float(value)
        elif expected_type == str:
            value = _sanitize_string(str(value))
        elif expected_type == list:
            if not isinstance(value, list):
                return default
            # Validate each element is a safe string
            value = [_sanitize_string(str(item)) for item in value
                     if isinstance(item, (str, int))]
    except (ValueError, TypeError):
        return default

    # ── Range checks ──────────────────────────────────────────────────────────
    if expected_type in (int, float) and min_val is not None and max_val is not None:
        value = max(min_val, min(max_val, value))

    # ── Allowlist checks ──────────────────────────────────────────────────────
    if key == "theme" and value not in _VALID_THEMES:
        return default
    if key == "typing_mode" and value not in _VALID_TYPING_MODES:
        return default
    if key == "language" and value not in _VALID_LANGUAGES:
        return default
    if key == "game_rotation":
        value = [g for g in value if g in _VALID_GAMES]
        if not value:
            return default

    return value


def load_config() -> dict:
    """
    Load config from disk. Validates every field.
    Unknown/malformed keys are dropped. Missing keys get defaults.
    Returns a guaranteed-safe dict — never raises.
    """
    config_path = _get_config_path()
    raw: dict = {}

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read(65536)  # 64 KB cap — config should never be larger
                raw = json.loads(content)
            if not isinstance(raw, dict):
                raw = {}
        except (json.JSONDecodeError, OSError, MemoryError):
            raw = {}

    # Build validated config: start from defaults, overlay validated values
    validated: dict = {}
    for key, (_, _, _, default) in _SCHEMA.items():
        incoming = raw.get(key, default)
        validated[key] = _validate_field(key, incoming)

    return validated


def save_config(config: dict) -> bool:
    """
    Validate and save config to disk as JSON.
    Returns True on success, False on failure.
    Never writes unvalidated data.
    """
    config_path = _get_config_path()

    # Re-validate everything before writing — never trust in-memory state blindly
    safe: dict = {}
    for key in _SCHEMA:
        value = config.get(key, _SCHEMA[key][3])
        safe[key] = _validate_field(key, value)

    try:
        # Write to temp file first, then atomic rename (prevents corrupt config on crash)
        tmp_path = config_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(safe, f, indent=2, ensure_ascii=False)
        tmp_path.replace(config_path)
        return True
    except OSError:
        return False


def get_default_config() -> dict:
    """Return a fresh config with all defaults."""
    return {key: default for key, (_, _, _, default) in _SCHEMA.items()}


def get_config_path() -> Path:
    """Public accessor for config file location (used in settings UI)."""
    return _get_config_path()
