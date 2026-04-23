"""
QiyamBreak - Fullscreen Break Overlay
The main break window. Covers all screens. Cannot be accidentally closed.
Dismiss button locked for minimum break_seconds.
"""

import random
from typing import Callable, Optional

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QScrollArea, QSizePolicy,
)
from PyQt6.QtGui import QScreen, QGuiApplication

from content_loader import content
from theme_manager import theme_manager
from games import TypingGame, ReflexGame, MathGame, BreathingGame, PostureCheck


class BreakOverlay(QWidget):
    """
    Fullscreen break overlay.
    - Covers all monitors (uses the primary screen)
    - Dismiss button disabled for `break_seconds`
    - Shows: task, dua corner, optional game, reminder quote
    - Emits `dismissed` signal with session stats
    """

    dismissed = pyqtSignal(dict)  # emits stats dict

    def __init__(
        self,
        config: dict,
        on_stats: Optional[Callable[[dict], None]] = None,
    ) -> None:
        super().__init__(None)
        self._config = config
        self._on_stats = on_stats
        self._break_seconds: int = max(30, int(config.get("break_seconds", 120)))
        self._remaining: int = self._break_seconds
        self._game_result: dict = {}

        # Theme
        theme_id = config.get("theme", "fajr_dawn")
        if config.get("random_theme", False):
            theme = theme_manager.get_random_theme()
        else:
            theme = theme_manager.get_theme(theme_id)
        self._theme = theme

        # Window setup — frameless, always on top, covers everything
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setObjectName("OverlayWindow")

        # Apply theme stylesheet
        self.setStyleSheet(theme_manager.build_overlay_qss(theme))

        self._build_ui()
        self._start_countdown()

        # Cover all screens
        screen: QScreen = QGuiApplication.primaryScreen()
        self.setGeometry(screen.geometry())

    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)

        # ── Top bar: title + countdown ────────────────────────────────────────
        top_bar = QHBoxLayout()

        title = QLabel("🕌  QiyamBreak — Time to Move")
        title.setObjectName("TitleLabel")
        top_bar.addWidget(title)

        top_bar.addStretch()

        self._countdown_label = QLabel(f"Dismiss in {self._remaining}s")
        self._countdown_label.setObjectName("CountdownLabel")
        top_bar.addWidget(self._countdown_label)

        main_layout.addLayout(top_bar)

        # ── Divider ───────────────────────────────────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {self._theme.get('card_border', '#333')};")
        main_layout.addWidget(line)

        # ── Middle: task card + game card (side by side) ─────────────────────
        middle = QHBoxLayout()
        middle.setSpacing(24)

        # Task card
        task_card = self._build_task_card()
        middle.addWidget(task_card, 3)

        # Game card (optional)
        if self._config.get("show_games", True):
            game_card = self._build_game_card()
            if game_card:
                middle.addWidget(game_card, 4)

        main_layout.addLayout(middle, 1)

        # ── Dua card (bottom) ─────────────────────────────────────────────────
        if self._config.get("show_duas", True):
            dua_card = self._build_dua_card()
            main_layout.addWidget(dua_card)

        # ── Reminder quote ────────────────────────────────────────────────────
        reminder = content.get_reminder()
        if reminder:
            rem_label = QLabel(f'"{reminder["text"]}" — {reminder["source"]}')
            rem_label.setObjectName("ReminderLabel")
            rem_label.setWordWrap(True)
            rem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(rem_label)

        # ── Dismiss button ────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._dismiss_btn = QPushButton("⏳  Stand up first…")
        self._dismiss_btn.setObjectName("DismissButton")
        self._dismiss_btn.setEnabled(False)
        self._dismiss_btn.clicked.connect(self._dismiss)
        btn_row.addWidget(self._dismiss_btn)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

    def _build_task_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("TaskCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        task = content.get_task()
        if not task:
            task = {
                "icon": "🚶", "title": "Walk Around",
                "instruction": "Stand up and walk for 1 minute.",
                "duration_seconds": 60
            }

        icon_label = QLabel(task["icon"])
        icon_label.setObjectName("TaskIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        title_label = QLabel(task["title"])
        title_label.setObjectName("TaskTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        instr_label = QLabel(task["instruction"])
        instr_label.setObjectName("TaskInstruction")
        instr_label.setWordWrap(True)
        instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instr_label)

        return card

    def _build_dua_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("DuaCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(6)

        dua = content.get_dua()
        if not dua:
            return card

        # Arabic — right-aligned
        arabic = QLabel(dua["arabic"])
        arabic.setObjectName("ArabicLabel")
        arabic.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        arabic.setWordWrap(True)
        layout.addWidget(arabic)

        # Transliteration
        translit = QLabel(dua["transliteration"])
        translit.setObjectName("TranslitLabel")
        translit.setWordWrap(True)
        layout.addWidget(translit)

        # Meaning
        meaning = QLabel(f'"{dua["meaning"]}"')
        meaning.setObjectName("MeaningLabel")
        meaning.setWordWrap(True)
        layout.addWidget(meaning)

        # Source
        source = QLabel(f"— {dua['source']}")
        source.setObjectName("SourceLabel")
        layout.addWidget(source)

        return card

    def _build_game_card(self) -> Optional[QFrame]:
        rotation: list = self._config.get("game_rotation", [])
        if not rotation:
            return None

        game_type = random.choice(rotation)
        card = QFrame()
        card.setObjectName("GameCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)

        game_widget = None
        if game_type == "typing":
            mode = self._config.get("typing_mode", "accuracy")
            game_widget = TypingGame(mode=mode)
        elif game_type == "reflex":
            game_widget = ReflexGame()
        elif game_type == "math":
            game_widget = MathGame()
        elif game_type == "breathing":
            game_widget = BreathingGame()
        elif game_type == "posture":
            game_widget = PostureCheck()

        if game_widget:
            game_widget.finished.connect(self._on_game_finished)
            layout.addWidget(game_widget)
            return card

        return None

    # ── Countdown ─────────────────────────────────────────────────────────────

    def _start_countdown(self):
        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._tick_countdown)
        self._countdown_timer.start(1000)

    def _tick_countdown(self):
        self._remaining -= 1
        if self._remaining <= 0:
            self._countdown_timer.stop()
            self._countdown_label.setText("You may dismiss ✓")
            self._dismiss_btn.setText("✓  I'm up! Jazakallahu khairan")
            self._dismiss_btn.setEnabled(True)
        else:
            self._countdown_label.setText(f"Dismiss in {self._remaining}s")

    # ── Events ────────────────────────────────────────────────────────────────

    def _on_game_finished(self, result: dict):
        self._game_result = result

    def _dismiss(self):
        if not self._dismiss_btn.isEnabled():
            return  # Safety — shouldn't happen but guard it
        self._countdown_timer.stop()
        stats = {
            "break_duration": self._break_seconds - max(self._remaining, 0),
            "game_result": self._game_result,
        }
        self.dismissed.emit(stats)
        self.close()

    def keyPressEvent(self, event):
        """Block Alt+F4, Escape, etc. during minimum break period."""
        if not self._dismiss_btn.isEnabled():
            event.ignore()
            return
        # After minimum time, allow Escape to dismiss
        if event.key() == Qt.Key.Key_Escape:
            self._dismiss()
        else:
            event.ignore()

    def closeEvent(self, event):
        """Block window close during minimum break period."""
        if not self._dismiss_btn.isEnabled():
            event.ignore()
        else:
            event.accept()
