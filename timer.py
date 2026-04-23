"""
QiyamBreak - Timer Logic
Tracks sitting time and fires break callbacks.
Thread-safe. No global state mutations outside the class.
"""

import threading
import time
from typing import Callable, Optional


class SittingTimer:
    """
    Tracks elapsed sitting time and triggers a break callback
    when the configured interval is reached.

    Thread-safe: uses threading.Event for clean stop/pause/resume.
    """

    def __init__(
        self,
        sit_minutes: int,
        on_break: Callable[[], None],
        on_tick: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Args:
            sit_minutes:  How many minutes before a break is triggered.
            on_break:     Callback fired when break time is reached.
            on_tick:      Optional callback fired every second with
                          (elapsed_seconds, total_seconds).
        """
        self._sit_seconds: int = max(5 * 60, min(180 * 60, sit_minutes * 60))
        self._on_break = on_break
        self._on_tick = on_tick

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
        """Start the sitting timer."""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._stop_event.clear()
            self._pause_event.set()
            self._elapsed = 0
            self._thread = threading.Thread(
                target=self._run, daemon=True, name="QiyamBreak-Timer"
            )
            self._thread.start()

    def stop(self) -> None:
        """Stop and reset the timer."""
        with self._lock:
            self._running = False
            self._stop_event.set()
            self._pause_event.set()  # Unblock if paused

    def pause(self) -> None:
        """Pause the timer (e.g. user is on a break)."""
        self._pause_event.clear()
        self._paused = True

    def resume(self) -> None:
        """Resume the timer after a break."""
        self._elapsed = 0  # Reset on resume — fresh sitting session
        self._paused = False
        self._pause_event.set()

    def reset(self) -> None:
        """Reset elapsed time without stopping."""
        with self._lock:
            self._elapsed = 0

    def update_sit_minutes(self, sit_minutes: int) -> None:
        """Live-update the sitting duration (validated)."""
        self._sit_seconds = max(5 * 60, min(180 * 60, sit_minutes * 60))

    @property
    def elapsed_seconds(self) -> int:
        return self._elapsed

    @property
    def remaining_seconds(self) -> int:
        return max(0, self._sit_seconds - self._elapsed)

    @property
    def progress(self) -> float:
        """0.0 to 1.0 — how far through the sit window we are."""
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
        while not self._stop_event.is_set():
            # Block here while paused
            self._pause_event.wait()

            if self._stop_event.is_set():
                break

            time.sleep(1)

            if self._stop_event.is_set():
                break

            if not self._pause_event.is_set():
                continue  # Just became paused between sleep and here

            with self._lock:
                self._elapsed += 1
                elapsed = self._elapsed
                total = self._sit_seconds

            # Fire tick callback (safe — no lock held)
            if self._on_tick:
                try:
                    self._on_tick(elapsed, total)
                except Exception:
                    pass  # Never let UI callback crash the timer thread

            # Check if break time reached
            if elapsed >= total:
                try:
                    self._on_break()
                except Exception:
                    pass
                # Pause self — timer resumes only after break is dismissed
                self.pause()

        with self._lock:
            self._running = False
