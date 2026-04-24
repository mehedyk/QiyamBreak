# -*- mode: python ; coding: utf-8 -*-
# QiyamBreak PyInstaller spec file
# Builds a single-file executable for Windows (.exe) and Linux (binary)
#
# Usage:
#   Windows: pyinstaller qiyambreak.spec
#   Linux:   pyinstaller qiyambreak.spec

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include all content JSON files
        ('content/*.json', 'content'),
        # Include themes
        ('themes/*.json', 'themes'),
        # Include assets (icons, fonts if any)
        ('assets/', 'assets'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unused heavy modules to keep binary small
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QiyamBreak',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,            # Compress the binary (smaller file size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # No console window on Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows icon (comment out on Linux)
    icon='assets/icons/qiyambreak.ico',
)
