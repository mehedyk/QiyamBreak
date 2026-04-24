# QiyamBreak — Privacy Policy

**Version:** 1.0  
**Effective Date:** 2026-04-23  
**Author:** S.M. Mehedy Kawser
**Contact:** github.com/mehedyk

---

## The Short Version (Plain Language)

QiyamBreak **collects nothing about you.**

- No internet connection is ever made
- No data leaves your device — ever
- No accounts, no sign-up, no email
- No analytics, no crash reports, no telemetry
- No advertising, no tracking pixels, no third-party SDKs
- The only file this app creates is a settings file on **your own computer**

That is the entire privacy story. Everything below is the formal version of the same truth.

---

## 1. Who We Are

QiyamBreak is an open-source desktop application built by S.M. Mehedy Kawser. It is a personal, non-commercial project built with the intention of benefiting the Muslim community and all desk workers.

---

## 2. What Data Is Collected

**None.**

QiyamBreak does not collect, store, transmit, or process any personal data. There is no server, no database, no API endpoint that receives your information.

---

## 3. What Is Stored Locally on Your Device

QiyamBreak creates **one file** on your computer:

**File location:**
- Windows: `C:\Users\<you>\AppData\Roaming\QiyamBreak\config.json`
- Linux: `~/.config/QiyamBreak/config.json`

**Contents of that file:**

| Field | What it is | Example |
|-------|-----------|---------|
| `sit_minutes` | Your timer setting | `30` |
| `break_seconds` | Minimum break length | `120` |
| `theme` | Your chosen overlay theme | `"fajr_dawn"` |
| `random_theme` | Whether theme is randomised | `false` |
| `show_games` | Games toggle | `true` |
| `show_duas` | Dua corner toggle | `true` |
| `show_tasks` | Tasks toggle | `true` |
| `typing_mode` | Typing game mode | `"accuracy"` |
| `sound_enabled` | Sound toggle | `true` |
| `start_on_boot` | Startup toggle | `false` |
| `language` | Language setting | `"en"` |
| `game_rotation` | Which games are in rotation | `["typing", "math"]` |
| `first_run` | Whether app has run before | `false` |
| `total_breaks_taken` | How many breaks you've taken | `47` |
| `typing_best_wpm` | Your typing personal best | `52.0` |
| `typing_best_accuracy` | Your accuracy personal best | `97.0` |

This file never leaves your device. It is never read by anyone except the app itself on your machine.

You can delete this file at any time. The app will recreate it with defaults on next launch.

---

## 4. Network Activity

**QiyamBreak makes zero network requests.**

There are no:
- Update checks
- Analytics pings
- Crash report uploads
- Cloud sync operations
- Ad network calls
- External API calls of any kind

You can verify this yourself by running QiyamBreak through a network monitor (e.g. Wireshark, Little Snitch, or any firewall). You will see no outbound connections.

---

## 5. Third-Party Services

**None.** QiyamBreak uses no third-party services, SDKs, libraries that phone home, or external dependencies beyond:

- **PyQt6** — a local GUI framework that runs entirely on your machine
- **Python standard library** — built-in modules, no network components used

---

## 6. Children's Privacy

QiyamBreak collects no data from anyone, including children. The app is safe for all ages.

---

## 7. Your Rights

Since we collect no data, there is nothing to access, correct, export, or delete — except the local config file described in Section 3, which you control entirely.

To "delete your data": delete the config file. That's it.

---

## 8. Open Source Verification

QiyamBreak is open source under QSAL v1.0. The full source code is available at:

**https://github.com/mehedyk/QiyamBreak**

You are welcome and encouraged to read the code and verify these claims yourself. The relevant files are:

- `config.py` — everything that is stored
- `main.py` — the entry point, no network calls
- `timer.py` — timer logic, no network calls
- `overlay.py` — overlay UI, no network calls

---

## 9. Changes to This Policy

If this policy ever changes (e.g. if a future version adds optional cloud sync), the change will be:

1. Documented in the changelog
2. Announced clearly in the app
3. Opt-in only — never automatic

---

## 10. Contact

For any questions about this privacy policy:

- GitHub: https://github.com/mehedyk
- Portfolio: https://mehedy.netlify.app

---

*"And do not spy on each other." — Al-Hujurat 49:12*

*We take this seriously.*
