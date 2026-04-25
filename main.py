"""
QiyamBreak — قيام بريك
Main entry point. Wires timer, tray, overlay, and settings together.

Author: S.M. Mehedy Kawser
License: QSAL v1.0
"""

import sys
import os

# ── Prevent multiple instances ─────────────────────────────────────────────────
def _single_instance_lock():
    """
    Return a lock object. If lock fails, another instance is running.
    Cross-platform: uses msvcrt on Windows, fcntl on Linux/macOS.
    """
    import tempfile
    lock_path = os.path.join(tempfile.gettempdir(), "qiyambreak.lock")
    try:
        lock_file = open(lock_path, "w")
        if sys.platform == "win32":
            import msvcrt
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_file  # Keep reference alive
    except (IOError, OSError):
        try:
            lock_file.close()
        except Exception:
            pass
        return None


from PyQt6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from PyQt6.QtCore import Qt, QTimer

from config import load_config, save_config
from content_loader import content
from theme_manager import theme_manager
from timer import SittingTimer
from tray import TrayIcon
from overlay import BreakOverlay
from settings import SettingsWindow
from about import AboutWindow


class QiyamBreakApp:
    """Main application controller."""

    def __init__(self, app: QApplication):
        self._app = app
        self._config = load_config()
        self._overlay: BreakOverlay | None = None
        self._settings_win: SettingsWindow | None = None
        self._about_win: AboutWindow | None = None
        self._break_triggered = False  # Guard against double-trigger

        # Load content and themes
        content.load()
        theme_manager.load()

        # Timer — no callbacks, polled from main thread via QTimer below
        self._timer = SittingTimer(
            sit_minutes=self._config["sit_minutes"],
        )

        # Tray
        self._tray = TrayIcon(
            on_pause_resume=self._on_pause_resume,
            on_test_break=self._show_overlay,
            on_settings=self._open_settings,
            on_about=self._open_about,
            on_quit=self._quit,
        )
        self._tray.show()

        # Main-thread poll timer — fires every second, 100% thread-safe
        self._poll_timer = QTimer()
        self._poll_timer.setInterval(1000)
        self._poll_timer.timeout.connect(self._poll)
        self._poll_timer.start()

        # Start background sit timer
        self._timer.start()

        # First-run welcome
        if self._config.get("first_run", True):
            self._tray.showMessage(
                "QiyamBreak is running 🕌",
                f"Will remind you every {self._config['sit_minutes']} minutes. "
                "Right-click the tray icon to configure.",
                QSystemTrayIcon.MessageIcon.Information,
                5000,
            )
            self._config["first_run"] = False
            save_config(self._config)

    def _poll(self):
        """
        Runs every second on the main thread via QTimer.
        Reads timer state and triggers break if time is up.
        No cross-thread calls — completely safe.
        """
        elapsed = self._timer.elapsed_seconds
        total = self._timer.sit_seconds

        # Update tray display
        self._tray.update_status(elapsed, total)

        # Trigger break when time is up
        if elapsed >= total and not self._break_triggered and not self._timer.is_paused:
            self._break_triggered = True
            self._timer.pause()
            self._tray.show_break_notification()
            self._show_overlay()

    def _show_overlay(self):
        """Show the break overlay. Safe to call from main thread only."""
        if self._overlay is not None:
            return  # Already showing
        self._overlay = BreakOverlay(config=self._config)
        self._overlay.dismissed.connect(self._on_break_dismissed)
        self._overlay.showFullScreen()

    def _on_break_dismissed(self, stats: dict):
        """Called when user dismisses the overlay."""
        self._overlay = None
        self._break_triggered = False  # Reset so next break can trigger

        # Update stats
        self._config["total_breaks_taken"] = self._config.get("total_breaks_taken", 0) + 1

        # Update typing personal bests
        game = stats.get("game_result", {})
        if game.get("game") == "typing":
            wpm = game.get("wpm", 0)
            acc = game.get("accuracy", 0)
            if wpm > self._config.get("typing_best_wpm", 0):
                self._config["typing_best_wpm"] = float(wpm)
            if acc > self._config.get("typing_best_accuracy", 0):
                self._config["typing_best_accuracy"] = float(acc)

        save_config(self._config)

        # Resume timer for next sitting session
        self._timer.resume()

    def _on_pause_resume(self, paused: bool):
        if paused:
            self._timer.pause()
        else:
            self._timer.resume()

    def _open_about(self):
        if self._about_win is not None:
            self._about_win.raise_()
            self._about_win.activateWindow()
            return
        self._about_win = AboutWindow(self._config, version="1.0.2")
        self._about_win.finished.connect(lambda _: setattr(self, "_about_win", None))
        self._about_win.show()

    def _open_settings(self):
        if self._settings_win is not None:
            self._settings_win.raise_()
            return

        self._settings_win = SettingsWindow(self._config)
        self._settings_win.config_saved.connect(self._on_config_saved)
        self._settings_win.finished.connect(lambda _: setattr(self, "_settings_win", None))
        self._settings_win.show()

    def _on_config_saved(self, new_config: dict):
        self._config = new_config
        # Apply new sit_minutes to running timer
        self._timer.update_sit_minutes(new_config["sit_minutes"])

    def _quit(self):
        save_config(self._config)
        self._poll_timer.stop()
        self._timer.stop()
        self._tray.hide()
        self._app.quit()


def main():
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running when windows close
    app.setApplicationName("QiyamBreak")
    app.setApplicationVersion("1.0.2")
    app.setOrganizationName("mehedyk")

    # Single instance check
    lock = _single_instance_lock()
    if lock is None:
        msg = QMessageBox()
        msg.setWindowTitle("QiyamBreak")
        msg.setText("QiyamBreak is already running.\nCheck your system tray.")
        msg.exec()
        sys.exit(0)

    # Check tray support
    if not QSystemTrayIcon.isSystemTrayAvailable():
        msg = QMessageBox()
        msg.setWindowTitle("QiyamBreak")
        msg.setText("System tray is not available on this desktop.\nQiyamBreak cannot run.")
        msg.exec()
        sys.exit(1)

    qb = QiyamBreakApp(app)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
