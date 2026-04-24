"""
QiyamBreak - Timer Logic
Tracks sitting time in a background thread.
State is read by the main thread via properties — no callbacks needed.
Thread-safe via threading.Lock.
"""

import threading
import time
from typing import Optional


class SittingTimer:
    """
    Tracks elapsed sitting time in a background thread.
    The main thread polls elapsed_seconds and sit_seconds via QTimer
    instead of using callbacks — avoids all cross-thread Qt issues.
    """

    def __init__(self, sit_minutes: int) -> None:
        """
        Args:
            sit_minutes: How many minutes before a break should be triggered.
                         Clamped to 5–180 minutes.
        """
        self._sit_seconds: int = max(5 * 60, min(180 * 60, sit_minutes * 60))
        self._elapsed: int = 0
        self._running: bool = False
        self._paused: bool = False

        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Not paused initially

        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    # ── Public API ─────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the sitting timer thread."""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._elapsed = 0
            self._stop_event.clear()
            self._pause_event.set()
            self._thread = threading.Thread(
                target=self._run, daemon=True, name="QiyamBreak-Timer"
            )
            self._thread.start()

    def stop(self) -> None:
        """Stop the timer thread."""
        self._stop_event.set()
        self._pause_event.set()  # Unblock if paused so thread can exit
        with self._lock:
            self._running = False

    def pause(self) -> None:
        """Pause elapsed time counting (e.g. during a break)."""
        self._paused = True
        self._pause_event.clear()

    def resume(self) -> None:
        """Resume counting with a fresh elapsed count."""
        with self._lock:
            self._elapsed = 0
        self._paused = False
        self._pause_event.set()

    def update_sit_minutes(self, sit_minutes: int) -> None:
        """Update the sitting duration live (validated, clamped)."""
        with self._lock:
            self._sit_seconds = max(5 * 60, min(180 * 60, sit_minutes * 60))

    def reset(self) -> None:
        """Reset elapsed time without stopping the thread."""
        with self._lock:
            self._elapsed = 0

    # ── Properties (read by main thread every second) ─────────────────────────

    @property
    def elapsed_seconds(self) -> int:
        with self._lock:
            return self._elapsed

    @property
    def sit_seconds(self) -> int:
        with self._lock:
            return self._sit_seconds

    @property
    def remaining_seconds(self) -> int:
        with self._lock:
            return max(0, self._sit_seconds - self._elapsed)

    @property
    def progress(self) -> float:
        """0.0 → 1.0, how far through the current sit window."""
        with self._lock:
            if self._sit_seconds == 0:
                return 0.0
            return min(1.0, self._elapsed / self._sit_seconds)

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def is_paused(self) -> bool:
        return self._paused

    # ── Internal ───────────────────────────────────────────────────────────────

    def _run(self) -> None:
        """Background thread — just increments elapsed every second."""
        while not self._stop_event.is_set():
            # Block here while paused
            self._pause_event.wait()

            if self._stop_event.is_set():
                break

            time.sleep(1)

            if self._stop_event.is_set():
                break

            if not self._pause_event.is_set():
                continue  # Became paused during sleep

            with self._lock:
                self._elapsed += 1

        with self._lock:
            self._running = False
