"""
QiyamBreak - Mini Games
PyQt6 widget implementations for all break games.
Each game is a self-contained QFrame that emits a 'finished' signal.
"""

import random
import time
from typing import Optional

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget,
)
from PyQt6.QtGui import QFont

from content_loader import content


# ── Base Game Frame ────────────────────────────────────────────────────────────

class BaseGame(QFrame):
    """All games inherit from this. Emits finished(result_dict) when done."""
    finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GameCard")
        self._start_time: Optional[float] = None

    def _elapsed_ms(self) -> int:
        if self._start_time is None:
            return 0
        return int((time.perf_counter() - self._start_time) * 1000)


# ── 1. Typing Game ─────────────────────────────────────────────────────────────

class TypingGame(BaseGame):
    """
    User types a displayed text passage.
    Tracks WPM (words per minute) and character accuracy.
    Supports 'accuracy' mode (no timer) and 'timed' mode (30s countdown).
    """

    def __init__(self, mode: str = "accuracy", parent=None):
        super().__init__(parent)
        self._mode = mode if mode in ("accuracy", "timed") else "accuracy"
        self._text_data = content.get_typing_text() or {
            "text": "Subhanallahi wa bihamdihi",
            "note": "Glory be to Allah and His is the praise."
        }
        self._target = self._text_data["text"]
        self._started = False
        self._timer: Optional[QTimer] = None
        self._time_left = 30  # for timed mode

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Header
        header = QLabel("⌨️  Typing Challenge")
        header.setObjectName("TaskTitle")
        layout.addWidget(header)

        # Mode badge
        mode_label = QLabel(
            "Accuracy Mode — no rush" if self._mode == "accuracy"
            else "Timed Mode — 30 seconds"
        )
        mode_label.setObjectName("SubtitleLabel")
        layout.addWidget(mode_label)

        # Target text display
        self._prompt_label = QLabel(self._target)
        self._prompt_label.setObjectName("TypingPrompt")
        self._prompt_label.setWordWrap(True)
        layout.addWidget(self._prompt_label)

        # Input field
        self._input = QLineEdit()
        self._input.setObjectName("TypingInput")
        self._input.setPlaceholderText("Start typing here…")
        self._input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self._input)

        # Note / context
        note = QLabel(self._text_data.get("note", ""))
        note.setObjectName("SourceLabel")
        note.setWordWrap(True)
        layout.addWidget(note)

        # Stats row (shown after completion)
        self._stats_frame = QFrame()
        stats_layout = QHBoxLayout(self._stats_frame)
        self._wpm_label = QLabel("")
        self._wpm_label.setObjectName("WpmLabel")
        self._acc_label = QLabel("")
        self._acc_label.setObjectName("AccuracyLabel")
        stats_layout.addWidget(self._wpm_label)
        stats_layout.addWidget(self._acc_label)
        self._stats_frame.hide()
        layout.addWidget(self._stats_frame)

        # Countdown (timed mode only)
        if self._mode == "timed":
            self._countdown_label = QLabel("⏱ 30s")
            self._countdown_label.setObjectName("CountdownLabel")
            layout.addWidget(self._countdown_label)

        self._input.setFocus()

    def _on_text_changed(self, typed: str):
        # Start timer on first keystroke
        if not self._started and typed:
            self._started = True
            self._start_time = time.perf_counter()
            if self._mode == "timed":
                self._timer = QTimer(self)
                self._timer.timeout.connect(self._tick_timer)
                self._timer.start(1000)

        # Accuracy mode: check for completion
        if self._mode == "accuracy":
            if typed == self._target:
                self._finish(typed)

        # Live coloring of prompt (green for correct chars, red for wrong)
        self._color_prompt(typed)

    def _color_prompt(self, typed: str):
        """Highlight correct/incorrect characters in the prompt."""
        result = ""
        for i, ch in enumerate(self._target):
            if i < len(typed):
                if typed[i] == ch:
                    result += f'<span style="color:#4caf50">{ch}</span>'
                else:
                    result += f'<span style="color:#f44336">{ch}</span>'
            else:
                result += ch  # unstyled, not yet typed
        self._prompt_label.setText(result)

    def _tick_timer(self):
        self._time_left -= 1
        if hasattr(self, "_countdown_label"):
            self._countdown_label.setText(f"⏱ {self._time_left}s")
        if self._time_left <= 0:
            if self._timer:
                self._timer.stop()
            self._finish(self._input.text())

    def _finish(self, typed: str):
        if self._timer:
            self._timer.stop()
        self._input.setReadOnly(True)

        elapsed_sec = self._elapsed_ms() / 1000.0
        wpm = self._calc_wpm(typed, elapsed_sec)
        accuracy = self._calc_accuracy(typed)

        self._wpm_label.setText(f"⚡ {wpm} WPM")
        self._acc_label.setText(f"🎯 {accuracy}% accuracy")
        self._stats_frame.show()

        result_msg = self._wpm_comment(wpm, accuracy)
        comment = QLabel(result_msg)
        comment.setObjectName("ReminderLabel")
        comment.setWordWrap(True)
        self.layout().addWidget(comment)

        self.finished.emit({
            "game": "typing",
            "wpm": wpm,
            "accuracy": accuracy,
            "elapsed_seconds": elapsed_sec,
        })

    @staticmethod
    def _calc_wpm(typed: str, elapsed_sec: float) -> int:
        if elapsed_sec < 0.5:
            return 0
        words = len(typed.split())
        return int((words / elapsed_sec) * 60)

    @staticmethod
    def _calc_accuracy(typed: str) -> int:
        target = content.get_typing_text()  # re-fetch won't help here
        # We need the target from instance — use a simple char comparison
        return 100  # Placeholder — instance method below overrides

    def _calc_accuracy_real(self, typed: str) -> int:
        if not self._target:
            return 100
        correct = sum(1 for a, b in zip(typed, self._target) if a == b)
        total = max(len(self._target), len(typed))
        return int((correct / total) * 100) if total > 0 else 100

    def _finish(self, typed: str):  # noqa: F811 — intentional override
        if self._timer:
            self._timer.stop()
        self._input.setReadOnly(True)

        elapsed_sec = max(self._elapsed_ms() / 1000.0, 0.5)
        wpm = self._calc_wpm(typed, elapsed_sec)
        accuracy = self._calc_accuracy_real(typed)

        self._wpm_label.setText(f"⚡ {wpm} WPM")
        self._acc_label.setText(f"🎯 {accuracy}% accuracy")
        self._stats_frame.show()

        comment = QLabel(self._wpm_comment(wpm, accuracy))
        comment.setObjectName("ReminderLabel")
        comment.setWordWrap(True)
        self.layout().addWidget(comment)

        self.finished.emit({
            "game": "typing",
            "wpm": wpm,
            "accuracy": accuracy,
            "elapsed_seconds": round(elapsed_sec, 1),
        })

    @staticmethod
    def _wpm_comment(wpm: int, accuracy: int) -> str:
        if accuracy < 70:
            return "Slow down, akh — accuracy over speed. The Prophet (ﷺ) said: 'Take things easy.'"
        if wpm < 20:
            return "Good start. Consistency is what matters — even dhikr is done one word at a time."
        if wpm < 40:
            return "Solid! Average typist range. Keep at it."
        if wpm < 60:
            return "Fast! Above average. Your fingers are making dhikr too 😄"
        if wpm < 80:
            return "Excellent! Developer-tier speed. MashAllah."
        return "SubhanAllah. Are you even human? 🔥"


# ── 2. Reflex Tap Game ─────────────────────────────────────────────────────────

class ReflexGame(BaseGame):
    """Buttons light up in sequence — tap them in order."""

    COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
    LABELS = ["🔴", "🔵", "🟢", "🟡", "🟣"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sequence: list[int] = []
        self._user_seq: list[int] = []
        self._score = 0
        self._build_ui()
        QTimer.singleShot(500, self._next_round)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title = QLabel("⚡ Reflex Tap")
        title.setObjectName("TaskTitle")
        layout.addWidget(title)

        self._instruction = QLabel("Watch the sequence, then repeat it!")
        self._instruction.setObjectName("SubtitleLabel")
        layout.addWidget(self._instruction)

        btn_row = QHBoxLayout()
        self._buttons = []
        for i in range(5):
            btn = QPushButton(self.LABELS[i])
            btn.setObjectName("GameButton")
            btn.setFixedSize(60, 60)
            btn.setFont(QFont("Segoe UI", 20))
            btn.clicked.connect(lambda checked, idx=i: self._user_tap(idx))
            btn.setEnabled(False)
            self._buttons.append(btn)
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)

        self._score_label = QLabel("Score: 0")
        self._score_label.setObjectName("CountdownLabel")
        layout.addWidget(self._score_label)

    def _next_round(self):
        self._sequence.append(random.randint(0, 4))
        self._user_seq = []
        self._instruction.setText(f"Watch… (sequence length: {len(self._sequence)})")
        for btn in self._buttons:
            btn.setEnabled(False)
        self._play_sequence(0)

    def _play_sequence(self, idx: int):
        if idx >= len(self._sequence):
            self._instruction.setText("Your turn! Tap in order.")
            for btn in self._buttons:
                btn.setEnabled(True)
            return
        btn = self._buttons[self._sequence[idx]]
        btn.setStyleSheet(f"background-color: white; border-radius: 6px;")
        QTimer.singleShot(400, lambda: self._reset_btn(btn, idx))

    def _reset_btn(self, btn: QPushButton, idx: int):
        btn.setStyleSheet("")
        QTimer.singleShot(200, lambda: self._play_sequence(idx + 1))

    def _user_tap(self, idx: int):
        self._user_seq.append(idx)
        pos = len(self._user_seq) - 1
        if self._user_seq[pos] != self._sequence[pos]:
            self._instruction.setText(f"Wrong! Final score: {self._score}")
            for btn in self._buttons:
                btn.setEnabled(False)
            self.finished.emit({"game": "reflex", "score": self._score})
            return
        if len(self._user_seq) == len(self._sequence):
            self._score += 1
            self._score_label.setText(f"Score: {self._score}")
            if self._score >= 5:  # End after 5 successful rounds
                self._instruction.setText(f"MashAllah! Score: {self._score} 🎉")
                for btn in self._buttons:
                    btn.setEnabled(False)
                self.finished.emit({"game": "reflex", "score": self._score})
            else:
                QTimer.singleShot(600, self._next_round)


# ── 3. Mental Math Game ────────────────────────────────────────────────────────

class MathGame(BaseGame):
    """Quick arithmetic — 5 questions, tracks score and time."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._questions = self._generate_questions(5)
        self._current = 0
        self._score = 0
        self._build_ui()
        self._show_question()

    def _generate_questions(self, n: int) -> list[tuple[str, int]]:
        questions = []
        for _ in range(n):
            a = random.randint(2, 20)
            b = random.randint(2, 20)
            op = random.choice(["+", "-", "×"])
            if op == "+":
                questions.append((f"{a} + {b}", a + b))
            elif op == "-":
                big, small = max(a, b), min(a, b)
                questions.append((f"{big} - {small}", big - small))
            else:
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                questions.append((f"{a} × {b}", a * b))
        return questions

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        title = QLabel("🧮 Mental Math")
        title.setObjectName("TaskTitle")
        layout.addWidget(title)

        self._progress_label = QLabel("Question 1 of 5")
        self._progress_label.setObjectName("SubtitleLabel")
        layout.addWidget(self._progress_label)

        self._question_label = QLabel("")
        self._question_label.setObjectName("TitleLabel")
        self._question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._question_label)

        self._answer_input = QLineEdit()
        self._answer_input.setObjectName("TypingInput")
        self._answer_input.setPlaceholderText("Your answer…")
        self._answer_input.returnPressed.connect(self._check_answer)
        layout.addWidget(self._answer_input)

        self._feedback = QLabel("")
        self._feedback.setObjectName("CountdownLabel")
        layout.addWidget(self._feedback)

        self._start_time = time.perf_counter()

    def _show_question(self):
        if self._current >= len(self._questions):
            self._end_game()
            return
        q, _ = self._questions[self._current]
        self._progress_label.setText(f"Question {self._current + 1} of {len(self._questions)}")
        self._question_label.setText(q)
        self._answer_input.clear()
        self._answer_input.setFocus()

    def _check_answer(self):
        raw = self._answer_input.text().strip()
        try:
            answer = int(raw)
        except ValueError:
            self._feedback.setText("Numbers only please!")
            return

        _, correct = self._questions[self._current]
        if answer == correct:
            self._score += 1
            self._feedback.setText("✓ Correct!")
        else:
            self._feedback.setText(f"✗ Answer was {correct}")

        self._current += 1
        QTimer.singleShot(700, self._show_question)

    def _end_game(self):
        elapsed = round(time.perf_counter() - self._start_time, 1)
        self._question_label.setText(f"{self._score}/5 correct in {elapsed}s")
        self._answer_input.hide()
        self._feedback.setText("Your brain is still working — alhamdulillah 🧠")
        self.finished.emit({"game": "math", "score": self._score, "elapsed": elapsed})


# ── 4. Breathing Pacer ────────────────────────────────────────────────────────

class BreathingGame(BaseGame):
    """Animated box breathing guide: 4 in, 4 hold, 4 out, 4 hold."""

    PHASES = [
        ("Breathe IN",  4, "#4caf50"),
        ("HOLD",        4, "#ff9800"),
        ("Breathe OUT", 4, "#2196f3"),
        ("HOLD",        4, "#9c27b0"),
    ]

    def __init__(self, cycles: int = 4, parent=None):
        super().__init__(parent)
        self._cycles_total = cycles
        self._cycle = 0
        self._phase = 0
        self._count = 0
        self._build_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        title = QLabel("🌬️  Box Breathing")
        title.setObjectName("TaskTitle")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self._phase_label = QLabel("Get ready…")
        self._phase_label.setObjectName("TitleLabel")
        self._phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._phase_label)

        self._count_label = QLabel("4")
        self._count_label.setObjectName("WpmLabel")
        self._count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self._count_label.font()
        font.setPointSize(48)
        self._count_label.setFont(font)
        layout.addWidget(self._count_label)

        self._cycle_label = QLabel(f"Cycle 1 of {self._cycles_total}")
        self._cycle_label.setObjectName("SubtitleLabel")
        self._cycle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._cycle_label)

        note = QLabel("Used by special forces for stress control.\nYour heart rate will drop within 2 cycles.")
        note.setObjectName("ReminderLabel")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)
        layout.addWidget(note)

    def _tick(self):
        name, duration, color = self.PHASES[self._phase]
        self._phase_label.setText(name)
        self._phase_label.setStyleSheet(f"color: {color};")
        self._count_label.setText(str(duration - self._count))
        self._count += 1

        if self._count >= duration:
            self._count = 0
            self._phase = (self._phase + 1) % len(self.PHASES)
            if self._phase == 0:
                self._cycle += 1
                self._cycle_label.setText(f"Cycle {self._cycle + 1} of {self._cycles_total}")
                if self._cycle >= self._cycles_total:
                    self._timer.stop()
                    self._phase_label.setText("Alhamdulillah ✓")
                    self._count_label.setText("🤲")
                    self.finished.emit({"game": "breathing", "cycles": self._cycle})


# ── 5. Posture Check ──────────────────────────────────────────────────────────

class PostureCheck(BaseGame):
    """Simple checklist — user ticks off good posture items."""

    CHECKS = [
        ("Feet flat on the floor", "Not dangling or crossed."),
        ("Back against the chair", "Lower back supported, not arched forward."),
        ("Screen at eye level", "Top of screen = eye level. Not looking up or down."),
        ("Elbows at 90°", "Arms relaxed, not raised or stretched."),
        ("Wrists straight", "Not bent up or down while typing."),
        ("Shoulders relaxed", "Not hunched up toward your ears."),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked: list[bool] = [False] * len(self.CHECKS)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        title = QLabel("🧱 Posture Check")
        title.setObjectName("TaskTitle")
        layout.addWidget(title)

        sub = QLabel("Fix each item, then check it off.")
        sub.setObjectName("SubtitleLabel")
        layout.addWidget(sub)

        self._check_buttons: list[QPushButton] = []
        for i, (item, tip) in enumerate(self.CHECKS):
            btn = QPushButton(f"  ☐  {item}")
            btn.setObjectName("GameButton")
            btn.setToolTip(tip)
            btn.clicked.connect(lambda checked, idx=i: self._toggle(idx))
            self._check_buttons.append(btn)
            layout.addWidget(btn)

        self._score_label = QLabel("0 / 6 fixed")
        self._score_label.setObjectName("CountdownLabel")
        layout.addWidget(self._score_label)

    def _toggle(self, idx: int):
        self._checked[idx] = not self._checked[idx]
        icon = "☑" if self._checked[idx] else "☐"
        item, _ = self.CHECKS[idx]
        self._check_buttons[idx].setText(f"  {icon}  {item}")
        count = sum(self._checked)
        self._score_label.setText(f"{count} / 6 fixed")
        if count == len(self.CHECKS):
            self._score_label.setText("Perfect posture! ✓ MashAllah")
            self.finished.emit({"game": "posture", "score": count})
