"""
QiyamBreak - About Window
Tabbed dialog: About / Privacy Policy / Terms of Use / System Requirements
All content rendered inside the app — no browser needed.
"""

from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QWidget, QLabel, QScrollArea, QPushButton,
    QFrame, QSizePolicy,
)
from PyQt6.QtGui import QFont, QDesktopServices

from theme_manager import theme_manager


_DOCS_DIR = Path(__file__).parent


def _load_md(filename: str) -> str:
    """Load a markdown file and return its text. Returns fallback on error."""
    path = _DOCS_DIR / filename
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return f"[{filename} not found. Please check your installation.]"


def _md_to_html(text: str) -> str:
    """
    Minimal Markdown → HTML converter for the subset we use.
    Handles: headings, bold, italic, tables, code, horizontal rules, links.
    No external library needed.
    """
    import re
    lines = text.split("\n")
    html_lines = []
    in_table = False
    in_code_block = False

    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code_block:
                html_lines.append("</pre>")
                in_code_block = False
            else:
                html_lines.append('<pre style="background:#1a1a1a;color:#e0e0e0;'
                                  'padding:8px;border-radius:4px;font-family:monospace;'
                                  'white-space:pre-wrap;font-size:12px;">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Horizontal rule
        if re.match(r"^---+$", line.strip()):
            html_lines.append('<hr style="border:none;border-top:1px solid #444;margin:12px 0;">')
            continue

        # Tables
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                in_table = True
                html_lines.append(
                    '<table style="border-collapse:collapse;width:100%;margin:8px 0;">'
                )
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.match(r"[-: ]+", c) for c in cells if c):
                continue  # separator row
            is_header = not any(html_lines[-2:]) or "thead" not in " ".join(html_lines[-3:])
            tag = "th" if in_table and len([l for l in html_lines if "<tr>" in l]) == 0 else "td"
            row = "".join(
                f'<{tag} style="border:1px solid #444;padding:4px 8px;text-align:left;">'
                f'{c}</{tag}>'
                for c in cells
            )
            html_lines.append(f"<tr>{row}</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False

        # Headings
        h_match = re.match(r"^(#{1,4})\s+(.*)", line)
        if h_match:
            level = len(h_match.group(1))
            sizes = {1: "20px", 2: "17px", 3: "15px", 4: "14px"}
            margins = {1: "16px 0 8px", 2: "14px 0 6px", 3: "10px 0 4px", 4: "8px 0 4px"}
            size = sizes.get(level, "14px")
            margin = margins.get(level, "8px 0 4px")
            content = _inline_md(h_match.group(2))
            html_lines.append(
                f'<p style="font-size:{size};font-weight:bold;margin:{margin};">{content}</p>'
            )
            continue

        # Blank line
        if not line.strip():
            if in_table:
                html_lines.append("</table>")
                in_table = False
            html_lines.append("<br>")
            continue

        # Regular paragraph
        html_lines.append(f'<p style="margin:3px 0;line-height:1.6;">{_inline_md(line)}</p>')

    if in_table:
        html_lines.append("</table>")
    if in_code_block:
        html_lines.append("</pre>")

    return "\n".join(html_lines)


def _inline_md(text: str) -> str:
    """Process inline markdown: bold, italic, code, links."""
    import re
    # Escape HTML first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Bold+italic
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(
        r"`([^`]+)`",
        r'<code style="background:#2a2a2a;padding:1px 4px;border-radius:3px;'
        r'font-family:monospace;font-size:12px;">\1</code>',
        text
    )
    # Links [text](url)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" style="color:#64b5f6;">\1</a>',
        text
    )
    return text


def _scrollable_text(html: str, theme: dict) -> QScrollArea:
    """Wrap HTML content in a scrollable area."""
    bg = theme.get("bg_solid", "#1a1a1a")
    text_p = theme.get("text_primary", "#f0f0f0")
    text_s = theme.get("text_secondary", "#aaaaaa")

    label = QLabel()
    label.setTextFormat(Qt.TextFormat.RichText)
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    label.setTextInteractionFlags(
        Qt.TextInteractionFlag.TextSelectableByMouse |
        Qt.TextInteractionFlag.LinksAccessibleByMouse
    )
    label.setStyleSheet(f"""
        QLabel {{
            color: {text_p};
            background-color: {bg};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 13px;
            padding: 16px;
            line-height: 1.6;
        }}
        QLabel a {{ color: #64b5f6; }}
    """)
    label.setText(html)

    scroll = QScrollArea()
    scroll.setWidget(label)
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(f"""
        QScrollArea {{
            background-color: {bg};
            border: none;
        }}
        QScrollBar:vertical {{
            background: {theme.get('card_bg', '#111')};
            width: 8px;
        }}
        QScrollBar::handle:vertical {{
            background: {theme.get('card_border', '#333')};
            border-radius: 4px;
        }}
    """)
    return scroll


class AboutWindow(QDialog):
    """
    About window with 5 tabs:
    About | Privacy Policy | Terms of Use | System Requirements | Changelog
    """

    def __init__(self, config: dict, version: str = "1.0.2", parent=None):
        super().__init__(parent)
        self._config = config
        self._version = version
        self.setWindowTitle("QiyamBreak — About")
        self.setMinimumSize(700, 560)
        self.setModal(False)  # Non-modal — user can use app while reading

        theme_id = config.get("theme", "fajr_dawn")
        self._theme = theme_manager.get_theme(theme_id)
        self.setStyleSheet(theme_manager.build_settings_qss(self._theme))

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header = self._build_header()
        layout.addWidget(header)

        # ── Tabs ──────────────────────────────────────────────────────────────
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._build_about_tab(), "ℹ️  About")
        tabs.addTab(self._build_doc_tab("PRIVACY_POLICY.md"), "🔒  Privacy")
        tabs.addTab(self._build_doc_tab("TERMS_OF_USE.md"), "📄  Terms")
        tabs.addTab(self._build_doc_tab("SYSTEM_REQUIREMENTS.md"), "💻  Requirements")
        tabs.addTab(self._build_doc_tab("CHANGELOG.md"), "📋  Changelog")
        layout.addWidget(tabs, 1)

        # ── Close button ──────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(16, 8, 16, 0)
        btn_row.addStretch()

        gh_btn = QPushButton("⭐  GitHub")
        gh_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/mehedyk/QiyamBreak"))
        )
        btn_row.addWidget(gh_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        btn_row.addWidget(close_btn)

        layout.addLayout(btn_row)

    def _build_header(self) -> QFrame:
        """Top banner with app name, version, tagline."""
        accent = self._theme.get("accent", "#e8952a")
        bg = self._theme.get("card_bg", "#111")
        text_p = self._theme.get("text_primary", "#f0f0f0")
        text_s = self._theme.get("text_secondary", "#aaa")

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-bottom: 2px solid {accent};
                padding: 0;
            }}
        """)
        frame.setFixedHeight(110)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(20)

        # Logo placeholder — programmatic "Q" in accent color
        logo = QLabel("🕌")
        logo.setStyleSheet("font-size: 48px; background: transparent;")
        layout.addWidget(logo)

        # App info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel("QiyamBreak  —  قيام بريك")
        name_label.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {text_p}; background: transparent;"
        )
        info_layout.addWidget(name_label)

        tagline = QLabel("Muslim-focused wellness break reminder for desk workers")
        tagline.setStyleSheet(f"font-size: 13px; color: {text_s}; background: transparent;")
        info_layout.addWidget(tagline)

        meta_row = QHBoxLayout()
        for label_text in [
            f"v{self._version}",
            "Python + PyQt6",
            "Windows & Linux",
            "QSAL v1.0",
            "Zero telemetry",
        ]:
            badge = QLabel(label_text)
            badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {self._theme.get('card_border', '#333')};
                    color: {text_s};
                    border-radius: 4px;
                    padding: 2px 8px;
                    font-size: 11px;
                    background: transparent;
                }}
            """)
            meta_row.addWidget(badge)
        meta_row.addStretch()
        info_layout.addLayout(meta_row)

        layout.addLayout(info_layout, 1)
        return frame

    def _build_about_tab(self) -> QWidget:
        """The main About tab with structured info cards."""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        bg = self._theme.get("bg_solid", "#1a1a1a")
        text_p = self._theme.get("text_primary", "#f0f0f0")
        text_s = self._theme.get("text_secondary", "#aaa")
        accent = self._theme.get("accent", "#e8952a")
        card_bg = self._theme.get("card_bg", "#111")
        card_bdr = self._theme.get("card_border", "#333")

        widget.setStyleSheet(f"background-color: {bg};")
        scroll.setStyleSheet(f"QScrollArea {{ background: {bg}; border: none; }}")

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(14)

        def section(title: str, rows: list[tuple[str, str]]) -> QFrame:
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {card_bdr};
                    border-radius: 8px;
                    padding: 4px;
                }}
            """)
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(16, 12, 16, 12)
            fl.setSpacing(8)

            title_lbl = QLabel(title)
            title_lbl.setStyleSheet(
                f"font-size: 14px; font-weight: bold; color: {accent}; background: transparent;"
            )
            fl.addWidget(title_lbl)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet(f"color: {card_bdr}; background: transparent;")
            fl.addWidget(line)

            for key, val in rows:
                row_layout = QHBoxLayout()
                row_layout.setSpacing(12)
                k = QLabel(key)
                k.setStyleSheet(
                    f"font-weight: bold; color: {text_s}; min-width: 160px; background: transparent;"
                )
                k.setFixedWidth(160)
                v = QLabel(val)
                v.setWordWrap(True)
                v.setOpenExternalLinks(True)
                v.setStyleSheet(f"color: {text_p}; background: transparent;")
                row_layout.addWidget(k)
                row_layout.addWidget(v, 1)
                fl.addLayout(row_layout)

            return frame

        # App info card
        layout.addWidget(section("Application", [
            ("Name", "QiyamBreak — قيام بريك"),
            ("Version", self._version),
            ("Platform", "Windows 10/11, Linux (x86_64)"),
            ("Framework", "Python 3.11+ with PyQt6"),
            ("License", "QSAL v1.0 — Source Available"),
            ("Source code", '<a href="https://github.com/mehedyk/QiyamBreak" '
                           'style="color:#64b5f6;">github.com/mehedyk/QiyamBreak</a>'),
        ]))

        # Author card
        layout.addWidget(section("Author", [
            ("Name", "S.M. Mehedy Kawser"),
            ("GitHub", '<a href="https://github.com/mehedyk" style="color:#64b5f6;">github.com/mehedyk</a>'),
            ("Portfolio", '<a href="https://mehedy.netlify.app" style="color:#64b5f6;">mehedy.netlify.app</a>'),
            ("Intention", "Built for the Muslim community and all desk workers"),
        ]))

        # Privacy summary card
        layout.addWidget(section("Privacy (Summary)", [
            ("Data collected", "None whatsoever"),
            ("Network requests", "Zero — app never connects to the internet"),
            ("Local storage", "One config file on your own device"),
            ("Analytics", "None"),
            ("Third-party SDKs", "None"),
            ("Full policy", "See Privacy tab above"),
        ]))

        # Health basis card
        layout.addWidget(section("Health Research Basis", [
            ("Back/neck pain prevalence", "53%+ of office workers (published research)"),
            ("Recommended break interval", "Every 25–45 minutes (ergonomics consensus)"),
            ("Break duration", "Even 2–5 minutes significantly reduces risk"),
            ("Disclaimer", "General guidance only — not medical advice"),
        ]))

        # Ayah
        ayah_frame = QFrame()
        ayah_frame.setStyleSheet(
            f"background-color: {card_bg}; border: 1px solid {card_bdr}; border-radius: 8px;"
        )
        ayah_layout = QVBoxLayout(ayah_frame)
        ayah_layout.setContentsMargins(20, 16, 20, 16)

        arabic = QLabel("وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ")
        arabic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arabic.setStyleSheet(
            f"font-family: 'Amiri', 'Scheherazade New', serif; "
            f"font-size: 20px; color: {self._theme.get('text_arabic', '#ddd')}; background: transparent;"
        )
        ayah_layout.addWidget(arabic)

        meaning = QLabel(
            '"And We have not sent you, [O Muhammad], except as a mercy to the worlds."\n'
            "— Al-Anbiya 21:107"
        )
        meaning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        meaning.setStyleSheet(
            f"font-style: italic; color: {text_s}; font-size: 13px; background: transparent;"
        )
        ayah_layout.addWidget(meaning)

        layout.addWidget(ayah_frame)
        layout.addStretch()

        return scroll

    def _build_doc_tab(self, filename: str) -> QScrollArea:
        """Generic tab that renders a markdown file."""
        raw = _load_md(filename)
        html = _md_to_html(raw)
        return _scrollable_text(html, self._theme)
