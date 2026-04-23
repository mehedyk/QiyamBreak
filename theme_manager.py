"""
QiyamBreak - Theme Manager
Loads themes from themes.json and returns QSS stylesheets.
"""

import json
import random
from pathlib import Path
from typing import Optional


_THEMES_PATH = Path(__file__).parent / "themes" / "themes.json"

_FALLBACK_THEME = {
    "id": "layl",
    "name": "Layl",
    "bg_solid": "#000000",
    "text_primary": "#f0f0f0",
    "text_secondary": "#aaaaaa",
    "text_arabic": "#dddddd",
    "accent": "#555555",
    "card_bg": "#111111",
    "card_border": "#333333",
    "button_bg": "#333333",
    "button_text": "#f0f0f0",
    "button_hover": "#444444",
}


class ThemeManager:
    def __init__(self) -> None:
        self._themes: dict[str, dict] = {}
        self._loaded = False

    def load(self) -> None:
        try:
            with open(_THEMES_PATH, "r", encoding="utf-8") as f:
                data = json.loads(f.read(65536))
            if isinstance(data, list):
                for t in data:
                    if isinstance(t, dict) and "id" in t:
                        self._themes[t["id"]] = t
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass
        self._loaded = True

    def get_theme(self, theme_id: str) -> dict:
        """Get theme by ID. Falls back to _FALLBACK_THEME if not found."""
        if not self._loaded:
            self.load()
        return self._themes.get(theme_id, _FALLBACK_THEME)

    def get_random_theme(self) -> dict:
        if not self._themes:
            return _FALLBACK_THEME
        return random.choice(list(self._themes.values()))

    def get_theme_names(self) -> list[tuple[str, str]]:
        """Returns list of (id, name) tuples for Settings dropdown."""
        if not self._loaded:
            self.load()
        return [(t["id"], t.get("name", t["id"])) for t in self._themes.values()]

    def build_overlay_qss(self, theme: dict) -> str:
        """Generate QSS stylesheet for the overlay window from theme dict."""
        bg        = theme.get("bg_solid", "#000000")
        text_p    = theme.get("text_primary", "#f0f0f0")
        text_s    = theme.get("text_secondary", "#aaaaaa")
        text_ar   = theme.get("text_arabic", "#dddddd")
        accent    = theme.get("accent", "#555555")
        card_bg   = theme.get("card_bg", "#111111")
        card_bdr  = theme.get("card_border", "#333333")
        btn_bg    = theme.get("button_bg", "#333333")
        btn_txt   = theme.get("button_text", "#f0f0f0")
        btn_hov   = theme.get("button_hover", "#444444")

        return f"""
        QWidget#OverlayWindow {{
            background-color: {bg};
        }}
        QLabel#TitleLabel {{
            color: {text_p};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 32px;
            font-weight: bold;
        }}
        QLabel#SubtitleLabel {{
            color: {text_s};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 16px;
        }}
        QLabel#ArabicLabel {{
            color: {text_ar};
            font-family: 'Amiri', 'Scheherazade New', 'Arial', serif;
            font-size: 22px;
            text-align: right;
        }}
        QLabel#TranslitLabel {{
            color: {text_s};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 14px;
            font-style: italic;
        }}
        QLabel#MeaningLabel {{
            color: {text_p};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 14px;
        }}
        QLabel#SourceLabel {{
            color: {accent};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 12px;
        }}
        QLabel#ReminderLabel {{
            color: {text_s};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 13px;
            font-style: italic;
        }}
        QLabel#CountdownLabel {{
            color: {accent};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 18px;
            font-weight: bold;
        }}
        QLabel#TaskIcon {{
            font-size: 48px;
        }}
        QLabel#TaskTitle {{
            color: {text_p};
            font-size: 22px;
            font-weight: bold;
        }}
        QLabel#TaskInstruction {{
            color: {text_s};
            font-size: 14px;
        }}
        QFrame#DuaCard {{
            background-color: {card_bg};
            border: 1px solid {card_bdr};
            border-radius: 12px;
        }}
        QFrame#TaskCard {{
            background-color: {card_bg};
            border: 1px solid {card_bdr};
            border-radius: 12px;
        }}
        QFrame#GameCard {{
            background-color: {card_bg};
            border: 1px solid {card_bdr};
            border-radius: 12px;
        }}
        QPushButton#DismissButton {{
            background-color: {btn_bg};
            color: {btn_txt};
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 32px;
        }}
        QPushButton#DismissButton:hover {{
            background-color: {btn_hov};
        }}
        QPushButton#DismissButton:disabled {{
            background-color: {card_bdr};
            color: {text_s};
        }}
        QPushButton#GameButton {{
            background-color: {accent};
            color: {btn_txt};
            border: none;
            border-radius: 6px;
            font-size: 14px;
            padding: 8px 20px;
        }}
        QPushButton#GameButton:hover {{
            background-color: {btn_hov};
        }}
        QLineEdit#TypingInput {{
            background-color: {card_bg};
            color: {text_p};
            border: 2px solid {card_bdr};
            border-radius: 6px;
            font-size: 15px;
            padding: 8px;
            font-family: 'Consolas', 'Courier New', monospace;
        }}
        QLineEdit#TypingInput:focus {{
            border: 2px solid {accent};
        }}
        QLabel#TypingPrompt {{
            color: {text_s};
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 15px;
        }}
        QLabel#WpmLabel {{
            color: {accent};
            font-size: 24px;
            font-weight: bold;
        }}
        QLabel#AccuracyLabel {{
            color: {text_p};
            font-size: 18px;
        }}
        QProgressBar#BreakProgress {{
            background-color: {card_bg};
            border: 1px solid {card_bdr};
            border-radius: 4px;
            height: 6px;
            text-visible: false;
        }}
        QProgressBar#BreakProgress::chunk {{
            background-color: {accent};
            border-radius: 4px;
        }}
        """

    def build_settings_qss(self, theme: dict) -> str:
        """Generate QSS for the settings window."""
        bg       = theme.get("bg_solid", "#1a1a1a")
        text_p   = theme.get("text_primary", "#f0f0f0")
        text_s   = theme.get("text_secondary", "#aaaaaa")
        card_bg  = theme.get("card_bg", "#111111")
        card_bdr = theme.get("card_border", "#333333")
        btn_bg   = theme.get("button_bg", "#333333")
        btn_txt  = theme.get("button_text", "#f0f0f0")
        btn_hov  = theme.get("button_hover", "#444444")
        accent   = theme.get("accent", "#555555")

        return f"""
        QDialog {{
            background-color: {bg};
            color: {text_p};
        }}
        QLabel {{
            color: {text_p};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        }}
        QGroupBox {{
            color: {text_s};
            border: 1px solid {card_bdr};
            border-radius: 8px;
            margin-top: 12px;
            padding: 8px;
            font-size: 13px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            color: {accent};
        }}
        QSlider::groove:horizontal {{
            background: {card_bdr};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background: {btn_bg};
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }}
        QSlider::sub-page:horizontal {{
            background: {accent};
            border-radius: 2px;
        }}
        QComboBox {{
            background-color: {card_bg};
            color: {text_p};
            border: 1px solid {card_bdr};
            border-radius: 4px;
            padding: 4px 8px;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QCheckBox {{
            color: {text_p};
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid {card_bdr};
            border-radius: 3px;
            background: {card_bg};
        }}
        QCheckBox::indicator:checked {{
            background: {accent};
            border-color: {accent};
        }}
        QPushButton {{
            background-color: {btn_bg};
            color: {btn_txt};
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {btn_hov};
        }}
        """


# Module-level singleton
theme_manager = ThemeManager()
