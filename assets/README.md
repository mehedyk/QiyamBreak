# QiyamBreak — Assets

Static assets bundled with the application.

## fonts/

Arabic and Latin fonts included for cross-platform text rendering.

| File | Family | Style | Used for |
|------|--------|-------|---------|
| NotoNaskhArabic-Regular.ttf | Noto Naskh Arabic | Regular | Dua Arabic text (Naskh/serif style) |
| NotoNaskhArabic-Bold.ttf | Noto Naskh Arabic | Bold | Dua Arabic headings |
| NotoSansArabic-Regular.ttf | Noto Sans Arabic | Regular | Transliteration, UI labels |
| NotoSansArabic-Bold.ttf | Noto Sans Arabic | Bold | UI headings |
| DejaVuSans.ttf | DejaVu Sans | Regular | Latin UI text fallback |
| DejaVuSans-Bold.ttf | DejaVu Sans | Bold | Latin UI headings fallback |

All fonts are licensed under the SIL Open Font License (OFL) — free to bundle and distribute.

## icons/

App icons in all required sizes.

| File | Size | Used for |
|------|------|---------|
| qiyambreak.ico | Multi-size (16/32/48/64/128/256px) | Windows executable icon |
| qiyambreak.png | 256×256px | Linux app icon (.desktop file) |
| qiyambreak_128x128.png | 128×128px | Linux high-res icon |
| qiyambreak_48x48.png | 48×48px | Linux standard icon |
| qiyambreak_32x32.png | 32×32px | Linux small icon |
| qiyambreak_16x16.png | 16×16px | Linux tray / taskbar |

Icon design: Navy circle with gold ring, crescent moon and star,
"Q" letter below — Fajr Dawn theme colours (#1B3A5C navy, #C8860A gold).

Note: The system tray icon shown while the app is running is generated
programmatically in tray.py and does not use these files.
These icons are for the OS application launcher and executable.
