# QiyamBreak — System Requirements

---

## Running from the Executable (Recommended for Most Users)

No Python installation needed. Just download and run.

### Windows

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Windows 10 (64-bit) | Windows 10/11 (64-bit) |
| RAM | 50 MB free | 100 MB free |
| Disk space | 80 MB | 80 MB |
| Display | 1024 × 768 | 1920 × 1080 or higher |
| System tray | Required | Required |
| Internet | Not required | Not required |
| Admin rights | Not required | Not required |

**Windows 7/8 are not supported.** PyQt6 requires Windows 10 or later.

### Linux

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Ubuntu 20.04 / Debian 11 / Fedora 34 or equivalent | Ubuntu 22.04+ / Fedora 38+ |
| Architecture | x86_64 (64-bit) | x86_64 (64-bit) |
| RAM | 50 MB free | 100 MB free |
| Disk space | 80 MB | 80 MB |
| Display | 1024 × 768 | 1920 × 1080 or higher |
| Desktop environment | Any with system tray support | KDE, XFCE, GNOME + AppIndicator |
| glibc | 2.17+ | 2.31+ |
| Internet | Not required | Not required |
| Admin rights | Not required | Not required |

**Wayland note:** QiyamBreak runs on Wayland via XWayland. The fullscreen overlay works correctly. If you experience tray icon issues, set `QT_QPA_PLATFORM=xcb` before launching.

---

## Running from Source (For Developers)

### Python Version

| Version | Status |
|---------|--------|
| Python 3.11 | ✅ Fully supported |
| Python 3.12 | ✅ Fully supported |
| Python 3.13 | ✅ Should work |
| Python 3.10 | ⚠️ May work, not tested |
| Python 3.9 or below | ❌ Not supported (uses 3.10+ syntax) |
| Python 2.x | ❌ Not supported |

### Required Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.6.0+ | GUI framework — windows, themes, widgets |
| pyinstaller | 6.0.0+ | Building executables (dev only) |

All other imports are from Python's standard library:
`json`, `os`, `sys`, `pathlib`, `threading`, `time`, `random`, `typing`, `fcntl` (Linux)

### Building the Executable

To build the `.exe` or Linux binary, you additionally need:

| Tool | Version | Notes |
|------|---------|-------|
| PyInstaller | 6.0.0+ | `pip install pyinstaller` |
| UPX (optional) | Any | Compresses the binary — smaller file size. Download from upx.github.io |

---

## System Tray Requirements

QiyamBreak lives in the system tray. Without tray support, it cannot run.

### Windows
System tray is built into Windows. No extra setup needed.

### Linux — Desktop Environment Compatibility

| Desktop | Tray Support | Notes |
|---------|-------------|-------|
| KDE Plasma | ✅ Native | Works out of the box |
| XFCE | ✅ Native | Works out of the box |
| MATE | ✅ Native | Works out of the box |
| LXDE / LXQt | ✅ Native | Works out of the box |
| GNOME 40+ | ⚠️ Needs extension | Install `gnome-shell-extension-appindicator` |
| GNOME 3.x | ⚠️ Needs extension | Same as above |
| i3 / sway | ⚠️ Needs tray bar | Use `polybar` or `stalonetray` |
| Hyprland | ⚠️ Needs tray | Use `waybar` with tray module |

**Installing GNOME AppIndicator extension:**
```bash
sudo apt install gnome-shell-extension-appindicator
# Then enable it in GNOME Extensions app or:
gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
```

---

## Display Requirements

- **Minimum resolution:** 1024 × 768
- **The fullscreen overlay** is designed for 1080p and above. It scales down gracefully but 768p will be tight.
- **Multi-monitor:** The overlay covers the primary monitor. Secondary monitor support is planned for v1.1.
- **HiDPI / 4K:** Fully supported via Qt's automatic scaling.
- **Dark/light mode:** QiyamBreak uses its own theming — unaffected by system dark/light mode.

---

## What QiyamBreak Does NOT Need

To be completely clear:

- ❌ No internet connection — ever
- ❌ No administrator/root privileges
- ❌ No special hardware (GPU, microphone, camera, sensors)
- ❌ No .NET framework (Windows)
- ❌ No Java runtime
- ❌ No Microsoft Visual C++ redistributables (bundled in the executable)
- ❌ No account or sign-up
- ❌ No cloud storage
- ❌ No antivirus exception (though Windows Defender may flag the PyInstaller binary — see Troubleshooting in DEPLOYMENT.md)

---

## Performance Impact

QiyamBreak is intentionally lightweight:

| Metric | Value |
|--------|-------|
| CPU usage (idle, ticking timer) | < 0.1% |
| RAM usage (tray only, no overlay) | ~30–50 MB |
| RAM usage (overlay open) | ~60–90 MB |
| Disk writes | Config save only — ~1 KB per save |
| Network usage | 0 bytes |

It will not slow down your machine, affect gaming performance, or interfere with other applications.

---

## Antivirus / Security Software

Some antivirus tools flag PyInstaller-built executables as suspicious. This is a **known false positive** — PyInstaller bundles a Python interpreter into the binary, which triggers heuristic detection.

**QiyamBreak is safe.** The full source code is publicly available for inspection at:  
https://github.com/mehedyk/QiyamBreak

If your antivirus flags it:
- Add `QiyamBreak.exe` to your exclusions list
- Or run from source (`python main.py`) — no antivirus concerns with Python scripts
- Or check VirusTotal — submit the file for multi-engine analysis

---

*Last updated: 2026-04-23*
