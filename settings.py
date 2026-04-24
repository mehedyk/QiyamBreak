"""
QiyamBreak - Settings Window
PyQt6 dialog for all user configuration.
Saves via config.py (validated). Never writes raw input directly.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QComboBox, QCheckBox,
    QPushButton, QTabWidget, QWidget, QSpacerItem,
    QSizePolicy, QListWidget, QListWidgetItem,
)

from config import load_config, save_config, get_config_path
from theme_manager import theme_manager


def _open_about_window(config: dict):
    """Standalone helper — settings.py can't import main.py (circular). Opens About directly."""
    from about import AboutWindow
    win = AboutWindow(config, version="1.0.0")
    win.exec()  # Modal when opened from settings


class SettingsWindow(QDialog):
    """Settings dialog. Emits config_saved(dict) when user saves."""
    config_saved = pyqtSignal(dict)

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self._config = dict(config)  # Work on a copy
        self.setWindowTitle("QiyamBreak — Settings")
        self.setMinimumWidth(540)
        self.setModal(True)

        # Apply theme
        theme = theme_manager.get_theme(self._config.get("theme", "fajr_dawn"))
        self.setStyleSheet(theme_manager.build_settings_qss(theme))

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel("⚙️  QiyamBreak Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self._build_timer_tab(), "⏱  Timer")
        tabs.addTab(self._build_appearance_tab(), "🎨  Themes")
        tabs.addTab(self._build_content_tab(), "📋  Content")
        tabs.addTab(self._build_games_tab(), "🎮  Games")
        tabs.addTab(self._build_about_tab(), "ℹ️  About")
        layout.addWidget(tabs)

        # Bottom buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        about_btn = QPushButton("ℹ️  About & Privacy")
        about_btn.clicked.connect(self._open_about)
        btn_row.addWidget(about_btn)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)

    # ── Timer Tab ──────────────────────────────────────────────────────────────

    def _build_timer_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        # Sitting duration
        sit_group = QGroupBox("Sitting Duration")
        sit_layout = QVBoxLayout(sit_group)

        sit_val = self._config.get("sit_minutes", 30)
        self._sit_value_label = QLabel(f"{sit_val} minutes")
        self._sit_value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        sit_layout.addWidget(self._sit_value_label)

        self._sit_slider = QSlider(Qt.Orientation.Horizontal)
        self._sit_slider.setMinimum(5)
        self._sit_slider.setMaximum(120)
        self._sit_slider.setValue(sit_val)
        self._sit_slider.setTickInterval(5)
        self._sit_slider.valueChanged.connect(
            lambda v: self._sit_value_label.setText(f"{v} minutes")
        )
        sit_layout.addWidget(self._sit_slider)

        note = QLabel("Recommended: 25–45 minutes. Research shows 30 min is the sweet spot.")
        note.setWordWrap(True)
        note.setStyleSheet("font-size: 12px; opacity: 0.7;")
        sit_layout.addWidget(note)
        layout.addWidget(sit_group)

        # Break duration
        break_group = QGroupBox("Minimum Break Duration")
        break_layout = QVBoxLayout(break_group)

        break_val = self._config.get("break_seconds", 120)
        self._break_value_label = QLabel(f"{break_val} seconds ({break_val // 60}m {break_val % 60}s)")
        self._break_value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        break_layout.addWidget(self._break_value_label)

        self._break_slider = QSlider(Qt.Orientation.Horizontal)
        self._break_slider.setMinimum(30)
        self._break_slider.setMaximum(300)
        self._break_slider.setValue(break_val)
        self._break_slider.setTickInterval(30)
        self._break_slider.valueChanged.connect(self._update_break_label)
        break_layout.addWidget(self._break_slider)

        note2 = QLabel("Minimum is 30 seconds — non-negotiable. Your spine needs it.")
        note2.setWordWrap(True)
        note2.setStyleSheet("font-size: 12px;")
        break_layout.addWidget(note2)
        layout.addWidget(break_group)

        # Startup
        startup_group = QGroupBox("System")
        startup_layout = QVBoxLayout(startup_group)
        self._startup_check = QCheckBox("Launch QiyamBreak when I turn on my computer")
        self._startup_check.setChecked(self._config.get("start_on_boot", False))
        startup_layout.addWidget(self._startup_check)

        self._sound_check = QCheckBox("Play a sound when break starts")
        self._sound_check.setChecked(self._config.get("sound_enabled", True))
        startup_layout.addWidget(self._sound_check)
        layout.addWidget(startup_group)

        layout.addStretch()
        return widget

    def _update_break_label(self, v: int):
        self._break_value_label.setText(f"{v} seconds ({v // 60}m {v % 60}s)")

    # ── Appearance Tab ─────────────────────────────────────────────────────────

    def _build_appearance_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        theme_group = QGroupBox("Overlay Theme")
        theme_layout = QVBoxLayout(theme_group)

        self._random_theme_check = QCheckBox("Random theme on every break (keeps it fresh)")
        self._random_theme_check.setChecked(self._config.get("random_theme", False))
        theme_layout.addWidget(self._random_theme_check)

        theme_layout.addWidget(QLabel("Or pick a fixed theme:"))

        self._theme_combo = QComboBox()
        theme_names = theme_manager.get_theme_names()
        current_theme = self._config.get("theme", "fajr_dawn")
        for i, (tid, tname) in enumerate(theme_names):
            self._theme_combo.addItem(tname, tid)
            if tid == current_theme:
                self._theme_combo.setCurrentIndex(i)
        theme_layout.addWidget(self._theme_combo)

        # Theme descriptions
        self._theme_desc = QLabel("")
        self._theme_desc.setWordWrap(True)
        self._theme_desc.setStyleSheet("font-size: 12px; font-style: italic;")
        self._theme_combo.currentIndexChanged.connect(self._update_theme_desc)
        self._update_theme_desc()
        theme_layout.addWidget(self._theme_desc)

        layout.addWidget(theme_group)
        layout.addStretch()
        return widget

    def _update_theme_desc(self):
        theme_id = self._theme_combo.currentData()
        if theme_id:
            theme = theme_manager.get_theme(theme_id)
            self._theme_desc.setText(theme.get("description", ""))

    # ── Content Tab ────────────────────────────────────────────────────────────

    def _build_content_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        content_group = QGroupBox("What to Show During Breaks")
        content_layout = QVBoxLayout(content_group)

        self._show_duas_check = QCheckBox("Show Dua corner (Arabic, transliteration, meaning, source)")
        self._show_duas_check.setChecked(self._config.get("show_duas", True))
        content_layout.addWidget(self._show_duas_check)

        self._show_tasks_check = QCheckBox("Show activity tasks (walk, stretch, water, etc.)")
        self._show_tasks_check.setChecked(self._config.get("show_tasks", True))
        content_layout.addWidget(self._show_tasks_check)

        self._show_games_check = QCheckBox("Show mini games")
        self._show_games_check.setChecked(self._config.get("show_games", True))
        content_layout.addWidget(self._show_games_check)

        layout.addWidget(content_group)

        typing_group = QGroupBox("Typing Game Mode")
        typing_layout = QVBoxLayout(typing_group)

        self._typing_accuracy = QCheckBox("Accuracy Mode (no time pressure — recommended for breaks)")
        self._typing_timed = QCheckBox("Timed Mode (30-second sprint)")
        mode = self._config.get("typing_mode", "accuracy")
        self._typing_accuracy.setChecked(mode == "accuracy")
        self._typing_timed.setChecked(mode == "timed")
        self._typing_accuracy.toggled.connect(lambda c: self._typing_timed.setChecked(not c))
        self._typing_timed.toggled.connect(lambda c: self._typing_accuracy.setChecked(not c))
        typing_layout.addWidget(self._typing_accuracy)
        typing_layout.addWidget(self._typing_timed)
        layout.addWidget(typing_group)

        layout.addStretch()
        return widget

    # ── Games Tab ─────────────────────────────────────────────────────────────

    def _build_games_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        label = QLabel("Select which games appear in the break rotation:")
        layout.addWidget(label)

        all_games = [
            ("typing",    "⌨️  Typing Challenge — WPM + accuracy"),
            ("reflex",    "⚡  Reflex Tap — sequence memory"),
            ("math",      "🧮  Mental Math — quick arithmetic"),
            ("breathing", "🌬️  Breathing Pacer — box breathing"),
            ("posture",   "🧱  Posture Check — fix your setup"),
        ]
        current_rotation = self._config.get("game_rotation", [g[0] for g in all_games])

        self._game_checks: dict[str, QCheckBox] = {}
        for gid, gname in all_games:
            cb = QCheckBox(gname)
            cb.setChecked(gid in current_rotation)
            self._game_checks[gid] = cb
            layout.addWidget(cb)

        note = QLabel("At least one game should be selected for the rotation to work.")
        note.setWordWrap(True)
        note.setStyleSheet("font-size: 12px;")
        layout.addWidget(note)

        layout.addStretch()
        return widget

    # ── About Tab ─────────────────────────────────────────────────────────────

    def _build_about_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        info_lines = [
            ("App", "QiyamBreak — قيام بريك"),
            ("Version", "1.0.0"),
            ("Author", "S.M. Mehedy Kawser"),
            ("GitHub", "github.com/mehedyk"),
            ("License", "QSAL v1.0 — See LICENSE file"),
            ("Config file", str(get_config_path())),
        ]
        for key, val in info_lines:
            row = QHBoxLayout()
            key_lbl = QLabel(f"{key}:")
            key_lbl.setStyleSheet("font-weight: bold; min-width: 100px;")
            val_lbl = QLabel(val)
            val_lbl.setWordWrap(True)
            row.addWidget(key_lbl)
            row.addWidget(val_lbl, 1)
            layout.addLayout(row)

        ayah = QLabel(
            '"And We have not sent you, [O Muhammad], except as a mercy to the worlds."\n'
            "— Al-Anbiya 21:107\n\n"
            "Built with the intention of benefiting the Muslim community\nand all desk workers. "
            "May Allah accept it."
        )
        ayah.setWordWrap(True)
        ayah.setStyleSheet("font-style: italic; margin-top: 20px;")
        layout.addWidget(ayah)

        layout.addStretch()
        return widget

    # ── Save ──────────────────────────────────────────────────────────────────

    def _open_about(self):
        _open_about_window(self._config)

    def _save(self):
        game_rotation = [gid for gid, cb in self._game_checks.items() if cb.isChecked()]
        if not game_rotation:
            game_rotation = ["typing"]  # Safety default

        new_config = dict(self._config)
        new_config.update({
            "sit_minutes":    self._sit_slider.value(),
            "break_seconds":  self._break_slider.value(),
            "theme":          self._theme_combo.currentData() or "fajr_dawn",
            "random_theme":   self._random_theme_check.isChecked(),
            "show_duas":      self._show_duas_check.isChecked(),
            "show_tasks":     self._show_tasks_check.isChecked(),
            "show_games":     self._show_games_check.isChecked(),
            "typing_mode":    "accuracy" if self._typing_accuracy.isChecked() else "timed",
            "sound_enabled":  self._sound_check.isChecked(),
            "start_on_boot":  self._startup_check.isChecked(),
            "game_rotation":  game_rotation,
        })

        if save_config(new_config):
            self._config = new_config
            self.config_saved.emit(new_config)
            self.accept()
        else:
            # Config save failed — silently keep dialog open
            title_label = self.findChild(QLabel)
            if title_label:
                title_label.setText("⚠️  Failed to save settings. Check disk permissions.")
