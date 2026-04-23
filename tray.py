"""
QiyamBreak - System Tray
Lives in the system tray. Right-click menu for all controls.
"""

import sys
from typing import Callable, Optional

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QTimer


def _make_tray_icon(color: str = "#e8952a", letter: str = "Q") -> QIcon:
    """
    Generate a simple tray icon programmatically.
    16x16 colored circle with a letter — no external assets needed.
    """
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Background circle
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 28, 28)

    # Letter
    painter.setPen(QColor("#ffffff"))
    font = QFont("Segoe UI", 14, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, letter)

    painter.end()
    return QIcon(pixmap)


class TrayIcon(QSystemTrayIcon):
    """
    System tray icon with right-click menu.
    Provides: status, pause/resume, test break, settings, quit.
    """

    def __init__(
        self,
        on_pause_resume: Callable[[bool], None],
        on_test_break: Callable[[], None],
        on_settings: Callable[[], None],
        on_about: Callable[[], None],
        on_quit: Callable[[], None],
        parent=None,
    ):
        super().__init__(parent)
        self._on_pause_resume = on_pause_resume
        self._on_test_break = on_test_break
        self._on_settings = on_settings
        self._on_about = on_about
        self._on_quit = on_quit
        self._paused = False

        self.setIcon(_make_tray_icon("#e8952a", "Q"))
        self.setToolTip("QiyamBreak — Tracking sitting time")

        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_menu(self):
        menu = QMenu()

        # Status (non-clickable header)
        self._status_action = menu.addAction("🟢  Running — 0:00 elapsed")
        self._status_action.setEnabled(False)
        menu.addSeparator()

        # Pause / Resume
        self._pause_action = menu.addAction("⏸  Pause")
        self._pause_action.triggered.connect(self._toggle_pause)
        menu.addSeparator()

        # Test break
        test_action = menu.addAction("🧪  Test Break Now")
        test_action.triggered.connect(self._on_test_break)

        # Settings
        settings_action = menu.addAction("⚙️  Settings")
        settings_action.triggered.connect(self._on_settings)

        # About
        about_action = menu.addAction("ℹ️  About / Privacy / Terms")
        about_action.triggered.connect(self._on_about)
        menu.addSeparator()

        # Quit
        quit_action = menu.addAction("✕  Quit QiyamBreak")
        quit_action.triggered.connect(self._on_quit)

        self.setContextMenu(menu)

    def _toggle_pause(self):
        self._paused = not self._paused
        if self._paused:
            self._pause_action.setText("▶  Resume")
            self.setIcon(_make_tray_icon("#888888", "Q"))
            self.setToolTip("QiyamBreak — Paused")
            self._status_action.setText("⏸  Paused")
        else:
            self._pause_action.setText("⏸  Pause")
            self.setIcon(_make_tray_icon("#e8952a", "Q"))
            self.setToolTip("QiyamBreak — Tracking sitting time")
        self._on_pause_resume(self._paused)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason):
        # Double-click or left-click → show/hide context menu
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._on_settings()

    def update_status(self, elapsed_seconds: int, total_seconds: int):
        """Update the tray tooltip and status menu item with elapsed time."""
        elapsed_min = elapsed_seconds // 60
        elapsed_sec = elapsed_seconds % 60
        remaining_min = (total_seconds - elapsed_seconds) // 60
        remaining_sec = (total_seconds - elapsed_seconds) % 60

        self._status_action.setText(
            f"🟢  {elapsed_min:02d}:{elapsed_sec:02d} elapsed — "
            f"{remaining_min:02d}:{remaining_sec:02d} until break"
        )
        self.setToolTip(
            f"QiyamBreak — Break in {remaining_min}m {remaining_sec}s"
        )

    def show_break_notification(self):
        """Show a system notification balloon when break starts."""
        self.showMessage(
            "QiyamBreak — Time to Move 🕌",
            "You've been sitting too long. Stand up, walk, and stretch.",
            QSystemTrayIcon.MessageIcon.Information,
            3000,
        )
