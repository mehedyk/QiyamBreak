# QiyamBreak — Changelog

All notable changes to QiyamBreak are documented here.  
Format: [Version] — Date — Summary

---

## [1.0.2] — 2026-04-23

### Initial Release 🎉

**Core:**
- Sitting timer — configurable 5 to 120 minutes
- Thread-safe timer with pause, resume, and reset
- Fullscreen break overlay — covers entire primary screen
- 30-second minimum break enforcement (dismiss button locked)
- Single-instance lock — prevents duplicate processes running
- Atomic config write — prevents config corruption on crash

**Overlay:**
- Random break task displayed each break
- Dua corner — Arabic, transliteration, English meaning, source
- Islamic reminder quote (hadith or Quranic ayah)
- Countdown timer showing seconds until dismiss is available
- Blocks Escape, Alt+F4, and window close during minimum break period

**13 Overlay Themes:**
- Fajr Dawn, Night of Qadr, Desert Sand, Al-Andalus
- Layl, Noor, Forest Dhikr, Madina Blue
- Amber Terminal, Kufic Geometry, Olive & Gold, Storm, Sakura
- Random theme option (different theme every break)

**Content:**
- 15 duas — themed by akhirah, health, ease, dhikr, salawat, tawakkul, etc.
- 12 break tasks — walk, water, stretch, eye rest, shoulder rolls, box breathing, dhikr walk, neck stretch, wall posture, calf raises, wrist stretch, window gazing
- 12 Islamic reminders — hadiths and ayahs on health, rest, dunya, gratitude
- 18 typing texts — transliterations, hadiths, tech quotes, wisdom

**5 Mini Games:**
- Typing Challenge — WPM + accuracy, personal best tracking, 18 varied texts
- Reflex Tap — sequence memory, progressive difficulty
- Mental Math — 5 arithmetic questions, score and time tracked
- Breathing Pacer — 4-cycle box breathing with animated phases
- Posture Check — 6-item interactive checklist

**System Tray:**
- Lives silently in the notification area
- Right-click menu: status, pause/resume, test break, settings, quit
- Live elapsed/remaining time in tooltip and menu
- System notification balloon when break fires
- Programmatic icon (no external asset needed)

**Settings GUI:**
- Timer tab — sit duration slider, break duration slider, startup toggle, sound toggle
- Themes tab — theme picker with description, random theme toggle
- Content tab — duas/tasks/games toggles, typing mode selector
- Games tab — per-game rotation toggles
- About tab — app info, author, config file location

**Security:**
- JSON-only config (no pickle, no eval, no exec)
- Every field type-checked and range-clamped on read AND write
- String sanitization — strips control characters
- File size caps on all JSON reads
- Unknown config keys silently discarded
- Atomic config save via temp file + rename

**Documentation:**
- README.md — full feature overview
- DEPLOYMENT.md — step-by-step guide for Python newcomers
- PRIVACY_POLICY.md — transparent data practices (none)
- TERMS_OF_USE.md — license, health disclaimer, Islamic content note
- SYSTEM_REQUIREMENTS.md — OS, RAM, display, tray compatibility
- CHANGELOG.md — this file
- LICENSE — QSAL v1.0

---

## [Upcoming — 2.0.0]

**Salah Waqt Integration:**
- Local prayer time calculation (adhanpy — no internet needed)
- Per-prayer daily tracking (Fajr, Dhuhr, Asr, Maghrib, Isha)
- Jumu'ah reminder on Fridays
- Yes/Not Yet response — tracks per-waqt confirmation
- Calculation method selector (MWL, ISNA, Hanafi, Karachi, etc.)
- Madhab selector for Asr time (Shafi'i vs Hanafi)

**Statistics Dashboard:**
- Breaks per day chart
- WPM history over time
- Total break time this week/month
- Streaks — consecutive days with all breaks taken

**Internationalisation:**
- Bengali (বাংলা) language toggle

---

*"The most beloved deeds to Allah are those done consistently, even if small."*  
*— Sahih al-Bukhari 6464*
