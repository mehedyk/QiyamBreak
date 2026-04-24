# QiyamBreak — Deployment Guide

Complete step-by-step guide for running and building QiyamBreak. Written for someone new to Python.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Python](#2-install-python)
3. [Get the Code](#3-get-the-code)
4. [Create a Virtual Environment](#4-create-a-virtual-environment)
5. [Inst1all Dependencies](#5-install-dependencies)
6. [Run from Source (Development)](#6-run-from-source-development)
7. [Using the App](#7-using-the-app)
8. [Build the Executable (.exe / Linux binary)](#8-build-the-executable)
9. [Run on Startup (Optional)](#9-run-on-startup-optional)
10. [Uninstalling](#10-uninstalling)
1. [Troubleshooting](#11-troubleshooting)

---

## 1. Prerequisites

**What you need before starting:**

| Tool | Windows | Linux |
|------|---------|-------|
| Python 3.11+ | Download from python.org | Usually pre-installed |
| Git | git-scm.com | `sudo apt install git` |
| pip | Comes with Python | Usually pre-installed |

**Check what you have** — open a terminal (Command Prompt or PowerShell on Windows, Terminal on Linux) and run:

```bash
python --version
# or on Linux:
python3 --version
```

You should see `Python 3.11.x` or higher. If you see `Python 2.x`, use `python3` everywhere in this guide instead of `python`.

---

## 2. Install Python

### Windows

1. Go to **https://www.python.org/downloads/**
2. Download the latest **Python 3.11** or **3.12** installer (64-bit)
3. Run the installer
4. ✅ **IMPORTANT: Check "Add Python to PATH"** at the very bottom of the installer screen — easy to miss
5. Click "Install Now"
6. Open a new Command Prompt and run `python --version` to confirm

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Linux (Fedora/RHEL)

```bash
sudo dnf install python3 python3-pip
python3 --version
```

---

## 3. Get the Code

**Option A — Git clone (recommended):**

```bash
git clone https://github.com/mehedyk/QiyamBreak
cd QiyamBreak
```

**Option B — Download ZIP:**

1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP to a folder of your choice
4. Open a terminal and `cd` into that folder

**How to `cd` into a folder:**

```bash
# Windows example:
cd C:\Users\YourName\Downloads\QiyamBreak

# Linux example:
cd ~/Downloads/QiyamBreak
```

**What you should see after getting the code:**

```
QiyamBreak/
├── main.py
├── timer.py
├── overlay.py
├── tray.py
├── settings.py
├── about.py
├── games.py
├── config.py
├── content_loader.py
├── theme_manager.py
├── content/
├── themes/
├── assets/
├── requirements.txt
├── qiyambreak.spec
├── LICENSE
├── README.md
├── DEPLOYMENT.md          ← you are reading this
├── PRIVACY_POLICY.md
├── TERMS_OF_USE.md
├── SYSTEM_REQUIREMENTS.md
└── CHANGELOG.md
```

If these files are all present, you have the full project.

---

## 4. Create a Virtual Environment

A virtual environment keeps QiyamBreak's dependencies separate from your system Python. This is best practice — always do this.

```bash
# Windows:
python -m venv venv

# Linux:
python3 -m venv venv
```

**Activate the virtual environment:**

```bash
# Windows (Command Prompt):
venv\Scripts\activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Linux:
source venv/bin/activate
```

After activation, your terminal prompt will show `(venv)` at the start. This means you're inside the virtual environment. All `pip install` commands from here only affect this project, not your whole system.

**To deactivate later (when you're done working on the project):**

```bash
deactivate
```

---

## 5. Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs exactly two packages:
- `PyQt6` — the GUI framework (windows, buttons, themes, the overlay)
- `pyinstaller` — for building the executable (you only need this if you want to build a `.exe` or Linux binary)

The install will take 1–3 minutes. You'll see a progress bar for each package.

**Verify the install worked:**

```bash
python -c "import PyQt6; print('PyQt6 OK')"
```

If you see `PyQt6 OK`, you're ready.

---

## 6. Run from Source (Development)

Make sure your virtual environment is activated, then:

```bash
# Windows:
python main.py

# Linux:
python3 main.py
```

QiyamBreak starts silently. No window appears — it goes straight to the system tray.

---

## 7. Using the App

### Finding the tray icon

**Windows:** Look at the bottom-right corner of your taskbar. Click the small **^** (up arrow) to reveal hidden tray icons. You'll see an orange circle with a **Q** — that's QiyamBreak.

**Linux:** Depends on your desktop. On KDE it's in the panel by default. On GNOME you need the AppIndicator extension (see Troubleshooting). On XFCE it appears in the notification area.

### Tray right-click menu

Right-click the **Q** icon to see:

```
🟢  Running — 00:00 elapsed — 30:00 until break   ← live status
─────────────────────────────────────────────────
⏸  Pause
─────────────────────────────────────────────────
🧪  Test Break Now          ← triggers the overlay immediately
⚙️  Settings                ← open the settings window
ℹ️  About / Privacy / Terms ← open the about window
─────────────────────────────────────────────────
✕  Quit QiyamBreak
```

### Testing the overlay

Click **"🧪 Test Break Now"** to immediately see what the break overlay looks like. The overlay will cover your entire screen — this is intentional. The dismiss button unlocks after 30 seconds.

### Settings window

Click **"⚙️ Settings"** to open the settings dialog. It has four tabs:

- **Timer** — sitting duration (5–120 min), minimum break length (30–300s), startup toggle, sound toggle
- **Themes** — pick from 13 themes or enable random theme mode
- **Content** — toggle duas, tasks, games; set typing game mode
- **Games** — choose which games appear in the break rotation

Click **"Save Settings"** to apply. Changes take effect on the next break.

### About window

Click **"ℹ️ About / Privacy / Terms"** in the tray menu to open the About window. It has five tabs:

- **About** — app info, author, health research basis, privacy summary
- **Privacy Policy** — full details of what is and isn't collected
- **Terms of Use** — license summary, health disclaimer, acceptable use
- **System Requirements** — OS, RAM, display, desktop environment compatibility
- **Changelog** — v1.0 features and v2.0 roadmap

You can also reach the About window from within Settings via the **"ℹ️ About & Privacy"** button at the bottom left of the settings dialog.

### Config file location

QiyamBreak saves your settings to a JSON file:

| OS | Path |
|----|------|
| Windows | `C:\Users\<you>\AppData\Roaming\QiyamBreak\config.json` |
| Linux | `~/.config/QiyamBreak/config.json` |

You can open this with any text editor — but use the Settings window instead, as it validates all values on save.

---

## 8. Build the Executable

Building creates a single file you can run on any machine without Python installed. Good for sharing or installing on another PC.

**Make sure your virtual environment is activated first.**

### Windows — build .exe

```bash
pyinstaller qiyambreak.spec
```

Wait 2–5 minutes. Output:

```
dist/
└── QiyamBreak.exe
```

Double-click `QiyamBreak.exe` to run. No Python needed.

**Antivirus note:** Windows Defender or other antivirus tools may flag the `.exe`. This is a known false positive with PyInstaller — it bundles a Python interpreter which triggers heuristic detection. QiyamBreak is open source and safe to inspect. To resolve: add `QiyamBreak.exe` to your antivirus exclusions, or run from source (`python main.py`) instead.

### Linux — build binary

```bash
pyinstaller qiyambreak.spec
```

Output: `dist/QiyamBreak`

Make it executable and run:

```bash
chmod +x dist/QiyamBreak
./dist/QiyamBreak
```

### Linux — add to app menu (.desktop file)

To make QiyamBreak appear in your application launcher, create a `.desktop` file:

```bash
nano ~/.local/share/applications/qiyambreak.desktop
```

Paste this (replace `/path/to` with your actual folder path):

```ini
[Desktop Entry]
Name=QiyamBreak
GenericName=Break Reminder
Comment=Muslim wellness break reminder for desk workers
Exec=/path/to/dist/QiyamBreak
Icon=/path/to/assets/icons/qiyambreak.png
Terminal=false
Type=Application
Categories=Utility;Health;
StartupNotify=false
Keywords=break;health;posture;islamic;muslim;
```

Save and close. It will appear in your app menu after a moment.

---

## 9. Run on Startup (Optional)

You can also toggle this inside the app: **Settings → Timer tab → "Launch QiyamBreak when I turn on my computer"**.

### Windows — startup folder method (manual)

1. Press `Win + R`, type `shell:startup`, press Enter
2. A folder opens — this is your Windows startup folder
3. Right-click inside → New → Shortcut
4. Browse to `dist/QiyamBreak.exe` (or `main.py` if running from source)
5. Name it "QiyamBreak" and click Finish

QiyamBreak will now start automatically on every boot.

### Linux — systemd user service

Create the service file:

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/qiyambreak.service
```

Paste (replace `/path/to` with your actual path):

```ini
[Unit]
Description=QiyamBreak wellness break reminder
After=graphical-session.target

[Service]
Type=simple
ExecStart=/path/to/dist/QiyamBreak
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Enable and start it:

```bash
systemctl --user enable qiyambreak
systemctl --user start qiyambreak
```

Check status:

```bash
systemctl --user status qiyambreak
```

### Linux — XDG autostart (simpler alternative)

```bash
mkdir -p ~/.config/autostart
cp ~/.local/share/applications/qiyambreak.desktop ~/.config/autostart/
```

This works on most desktops (KDE, XFCE, GNOME, MATE) without needing systemd.

---

## 10. Uninstalling

QiyamBreak does not use a traditional installer, so there's no uninstaller. To remove it completely:

**1. Quit the app** — right-click tray icon → Quit QiyamBreak

**2. Delete the project folder** — wherever you cloned or extracted it

**3. Delete the config file:**

```bash
# Windows (run in Command Prompt):
rmdir /s /q "%APPDATA%\QiyamBreak"

# Linux:
rm -rf ~/.config/QiyamBreak
```

**4. Remove startup entry (if you set one):**

- Windows: Delete the shortcut from `shell:startup`
- Linux systemd: `systemctl --user disable qiyambreak && systemctl --user stop qiyambreak`
- Linux XDG: `rm ~/.config/autostart/qiyambreak.desktop`

**5. Remove the virtual environment (if running from source):**

```bash
# Just delete the venv folder inside the project:
rm -rf venv/   # Linux
rmdir /s /q venv   # Windows
```

That's everything. No registry entries (Windows), no system files, no hidden data anywhere else.

---

## 11. Troubleshooting

### "python: command not found" (Linux)

Use `python3` instead of `python` everywhere:

```bash
python3 main.py
python3 -m venv venv
```

### "No module named PyQt6"

Your virtual environment is not activated. Run:

```bash
# Windows:
venv\Scripts\activate

# Linux:
source venv/bin/activate
```

Then try again.

### PowerShell says "running scripts is disabled" (Windows)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the venv again: `venv\Scripts\Activate.ps1`

### "No system tray available" (Linux / GNOME)

GNOME removed native system tray support. You need the AppIndicator extension:

```bash
sudo apt install gnome-shell-extension-appindicator
gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
```

Log out and back in. The tray icon will appear.

For other minimal desktops (i3, sway, Hyprland), use a standalone tray like `stalonetray` or configure your status bar (polybar, waybar) to include a tray module.

### Antivirus flags the .exe (Windows)

Expected with PyInstaller builds. Solutions in order of preference:

1. Add `dist\QiyamBreak.exe` to Windows Defender exclusions (Settings → Virus & threat protection → Exclusions)
2. Run from source with `python main.py` — Python scripts don't trigger this
3. Submit the file to VirusTotal for multi-engine verification

### The overlay doesn't cover my second monitor

Known limitation — the overlay covers the primary monitor only. Multi-monitor support is planned for v1.1. Workaround: set your main working monitor as the primary display in your OS display settings.

### Wayland tray icon not showing (Linux)

Force XWayland mode:

```bash
QT_QPA_PLATFORM=xcb python3 main.py
# or for the binary:
QT_QPA_PLATFORM=xcb ./dist/QiyamBreak
```

To make this permanent, edit the `.desktop` file and prefix the `Exec=` line with `env QT_QPA_PLATFORM=xcb`.

### Settings not saving / config file missing

QiyamBreak needs write access to its config directory:

```bash
# Check it exists and is writable:
# Linux:
ls -la ~/.config/QiyamBreak/

# Windows — check in File Explorer:
# C:\Users\<you>\AppData\Roaming\QiyamBreak\
```

If the folder doesn't exist, QiyamBreak creates it on first run. If it does exist but isn't writable, fix permissions:

```bash
# Linux:
chmod 755 ~/.config/QiyamBreak
```

### App starts but tray icon takes a moment to appear

Normal — give it 2–3 seconds on first launch. On Windows, check the hidden icons area (click ^ in the taskbar corner).

### About window / Privacy tab shows "[file not found]"

The documentation `.md` files must be in the same folder as `main.py`. If you moved the executable without the docs folder, copy them back. The About window reads them from disk at runtime.

---

*QiyamBreak v1.0 — Built by S.M. Mehedy Kawser. May Allah accept it.*
