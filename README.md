# QiyamBreak — قيام بريك

> *"Your body has a right over you."* — Sahih al-Bukhari 1975

A Muslim-focused wellness break reminder for Windows and Linux. Tracks your sitting time and fires a fullscreen break overlay when you've been sitting too long — with duas, Islamic reminders, break tasks, and mini games.

---

## Why This Exists

Over **53% of desk workers** suffer from regular back and neck pain.<br>
Over **73%** report feeling exhausted during the workday.<br>
Research confirms: **breaking sitting every 30–45 minutes significantly reduces musculoskeletal risk.**

QiyamBreak makes this automatic — and makes the breaks worth taking.

---

## Features

### Core
- ⏱ **Configurable sitting timer** — 5 to 120 minutes, adjustable anytime
- 🖥 **Fullscreen break overlay** — covers entire screen, cannot be accidentally closed
- 🔒 **Enforced minimum break** — 30-second floor, non-negotiable, user can increase it
- 🔔 **System tray** — lives silently in the notification area, zero taskbar clutter
- 🔁 **Single-instance lock** — prevents duplicate processes running

### Themes
- 🎨 **13 overlay themes** — each with full color palette, Arabic font support, QSS styling
- 🎲 **Random theme mode** — different theme every break

### Islamic Content
- 📿 **15 curated duas** — Arabic script, transliteration, English meaning, hadith/Quran source
- 📖 **12 Islamic reminders** — hadiths and Quranic ayahs on health, rest, dunya, and akhirah

### Break Activities
- 💪 **12 break tasks** — walk 30 steps, drink water, back stretch, eye rest, shoulder rolls, box breathing, dhikr walk, neck stretch, wall posture check, calf raises, wrist stretch, look outside

### Mini Games (5)
- ⌨️ **Typing Challenge** — WPM + accuracy stats, personal best tracking, 18 varied texts (transliterations, hadiths, tech quotes, wisdom)
- ⚡ **Reflex Tap** — sequence memory, progressive difficulty up to 5 rounds
- 🧮 **Mental Math** — 5 arithmetic questions, score + time tracked
- 🌬️ **Breathing Pacer** — 4-cycle box breathing with animated phase labels
- 🧱 **Posture Check** — 6-item interactive checklist

### Settings & Customisation
- ⚙️ **Full settings GUI** — tabbed window (Timer / Themes / Content / Games)
- 🎛 **Per-game rotation control** — toggle individual games on/off
- 🔊 **Sound toggle**, startup toggle, typing mode selector (accuracy vs timed)

### Transparency & Trust
- ℹ️ **About window** — in-app tabbed viewer for Privacy Policy, Terms, System Requirements, Changelog
- 🔒 **Zero telemetry** — no network requests, ever
- 🛡 **Secure config** — JSON only, validated on every read/write, no eval, no pickle, atomic save

---

## Screenshots

*Coming after v1.0 release.*

---

## Quick Start

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for the full step-by-step guide — Python setup, virtual environment, dependencies, building the executable. Written for someone new to Python.

**Short version (if you know Python):**

```bash
git clone https://github.com/mehedyk/QiyamBreak
cd QiyamBreak
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

QiyamBreak starts silently in your system tray. Right-click the orange **Q** icon to test a break or open settings.

---

## Building the Executable

```bash
# Windows (.exe) and Linux (binary) — same command:
pyinstaller qiyambreak.spec
```

Output: `dist/QiyamBreak.exe` (Windows) or `dist/QiyamBreak` (Linux)

No Python required on the target machine. See [DEPLOYMENT.md](DEPLOYMENT.md) for full details.

---

## Project Structure

```
QiyamBreak/
│
├── main.py                  # Entry point — wires timer, tray, overlay, settings, about
├── timer.py                 # Sitting timer (threaded, pause/resume/reset)
├── overlay.py               # Fullscreen break overlay window
├── tray.py                  # System tray icon and right-click menu
├── settings.py              # Settings window (tabbed PyQt6 dialog)
├── about.py                 # About window (Privacy / Terms / Requirements / Changelog tabs)
├── games.py                 # All 5 mini games (Typing, Reflex, Math, Breathing, Posture)
├── config.py                # Config load/save — strict JSON validation, no pickle
├── content_loader.py        # Loads and randomly selects duas, tasks, reminders, texts
├── theme_manager.py         # Theme loading and QSS stylesheet generation
│
├── content/
│   ├── duas.json            # 15 duas — Arabic, transliteration, meaning, source
│   ├── tasks.json           # 12 break activities with icons and instructions
│   ├── reminders.json       # 12 hadiths and Quranic reminders with notes
│   └── typing_texts.json    # 18 typing game texts across 4 categories
│
├── themes/
│   └── themes.json          # 13 theme definitions (colors, gradients, QSS values)
│
├── assets/
│   ├── fonts/               # Bundled fonts (Arabic + Latin)
│   └── icons/               # App icons (.ico for Windows, .png for Linux)
│
├── qiyambreak.spec          # PyInstaller build configuration
├── requirements.txt         # Python dependencies (PyQt6, pyinstaller)
│
├── LICENSE                  # QSAL v1.0 — read before forking or distributing
├── README.md                # This file
├── DEPLOYMENT.md            # Full step-by-step deployment guide
├── PRIVACY_POLICY.md        # What is collected (nothing) and what is stored (local only)
├── TERMS_OF_USE.md          # License summary, health disclaimer, acceptable use
├── SYSTEM_REQUIREMENTS.md   # OS, RAM, display, tray compatibility per desktop environment
└── CHANGELOG.md             # Version history and upcoming roadmap
```

---

## The 13 Themes

| # | Theme | Vibe |
|---|-------|------|
| 1 | **Fajr Dawn** | Blue-to-orange gradient, calm like pre-dawn |
| 2 | **Night of Qadr** | Deep purple, stars, mystical |
| 3 | **Desert Sand** | Warm Saharan beige and gold |
| 4 | **Al-Andalus** | Deep crimson and gold, Moorish |
| 5 | **Layl** | Pure black, minimal white — maximum focus |
| 6 | **Noor** | Clean bright white, clinical clarity |
| 7 | **Forest Dhikr** | Muted greens, earthy |
| 8 | **Madina Blue** | Cool teal and cyan, serene |
| 9 | **Amber Terminal** | Black + amber text — for developers |
| 10 | **Kufic Geometry** | Black + white Islamic geometric style |
| 11 | **Olive & Gold** | Olive green + gold, Quranic |
| 12 | **Storm** | Dark grey + red — for overdue break alerts |
| 13 | **Sakura** | Soft pink and white, gentle |

---

## Privacy

**QiyamBreak collects nothing. Makes zero network requests. Ever.**

The only file it creates is a local settings JSON on your own device. No accounts, no analytics, no telemetry, no third-party SDKs.

Full details: [PRIVACY_POLICY.md](PRIVACY_POLICY.md) — or open the app and go to **Tray → About / Privacy / Terms**.

---

## System Requirements

| | Windows | Linux |
|-|---------|-------|
| OS | Windows 10/11 (64-bit) | Ubuntu 20.04+ / Fedora 34+ or equivalent |
| RAM | 50 MB free | 50 MB free |
| Disk | 80 MB | 80 MB |
| Display | 1024×768 minimum | 1024×768 minimum |
| Python (source only) | 3.11+ | 3.11+ |
| Internet | Not required | Not required |

Full details including per-desktop-environment tray compatibility: [SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md)

---

## Documentation

| File | What's in it |
|------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Step-by-step: Python install → venv → run → build .exe |
| [PRIVACY_POLICY.md](PRIVACY_POLICY.md) | Exactly what is and isn't collected (nothing) |
| [TERMS_OF_USE.md](TERMS_OF_USE.md) | License summary, health disclaimer, acceptable use |
| [SYSTEM_REQUIREMENTS.md](SYSTEM_REQUIREMENTS.md) | OS, RAM, display, tray support per desktop |
| [CHANGELOG.md](CHANGELOG.md) | v1.0 feature list + v2.0 roadmap |
| [LICENSE](LICENSE) | QSAL v1.0 — full legal terms |

All of these are also readable **inside the app** via the About window — no browser needed.

---

## Accessing the About Window

Three ways to open it:

1. **Tray icon** → right-click → **ℹ️ About / Privacy / Terms**
2. **Settings window** → **ℹ️ About & Privacy** button (bottom left)
3. **Tray icon** → double-click → Settings → About & Privacy button

The About window has 5 tabs: About, Privacy Policy, Terms of Use, System Requirements, Changelog.

---

## Roadmap

### v1.0 — Current
Core timer, 13 themes, 5 games, duas, tasks, reminders, tray, settings, about window, full documentation, Windows + Linux builds.

### v2.0 — Planned
- Salah waqt reminders — local prayer time calculation (adhanpy, no internet needed)
- Per-prayer daily tracking — Fajr, Dhuhr, Asr, Maghrib, Isha
- Jumu'ah special reminder on Fridays
- Calculation method selector — MWL, ISNA, Hanafi, Karachi, etc.
- Statistics dashboard — breaks per day, WPM history, streaks
- Bengali (বাংলা) language toggle

### Future
- Rust + Tauri rewrite — smaller binary, better performance, same features

---

## License

**QSAL v1.0** — QiyamBreak Source Available License. Stricter than MIT.<br>
Read [LICENSE](LICENSE) before forking or distributing.<br>
Key points: personal use only, no commercial use, no redistribution without written permission.

---

## Contributing

Pull requests welcome for bug fixes and content additions (duas, typing texts, tasks). Read [LICENSE](LICENSE) Section 5 on contributions before submitting. For feature discussions, open a GitHub issue first.

---

## Author

**S.M. Mehedy Kawser (Klinger)**<br>
GitHub: [@mehedyk](https://github.com/mehedyk) | Portfolio: [mehedy.netlify.app](https://mehedy.netlify.app)<br>
Final-year BSc Software Engineering, Daffodil International University

*Built with the intention of benefiting the Muslim community and all desk workers. May Allah accept it.*

---

*"And We have not sent you, [O Muhammad], except as a mercy to the worlds." — Al-Anbiya 21:107*
