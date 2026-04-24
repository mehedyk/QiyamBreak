# -*- mode: python ; coding: utf-8 -*-
# QiyamBreak PyInstaller spec file
# Builds a single-file executable for Windows (.exe) and Linux (binary)
#
# Usage:
#   Windows: python -m PyInstaller qiyambreak.spec
#   Linux:   python -m PyInstaller qiyambreak.spec
#
# Before building, clean old artifacts:
#   Windows:  rmdir /s /q build dist
#   Linux:    rm -rf build dist

from PyInstaller.utils.hooks import collect_all

# Collect ALL PyQt6 components — DLLs, Qt plugins, platform drivers, etc.
# Without this, the .exe crashes with "No module named PyQt6" on other machines.
qt_datas, qt_binaries, qt_hiddenimports = collect_all('PyQt6')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=qt_binaries,
    datas=[
        # App content
        ('content/*.json', 'content'),
        ('themes/*.json',  'themes'),
        ('assets/',        'assets'),
        # PyQt6 runtime data (platform plugins, translations, etc.)
        *qt_datas,
    ],
    hiddenimports=qt_hiddenimports + [
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtNetwork',
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Strip heavy unused modules to keep binary size down
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
    upx=False,           # Set to True only if UPX is installed; False is safer
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # No console window on Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/qiyambreak.ico',
)
