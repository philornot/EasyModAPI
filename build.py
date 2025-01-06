"""
build.py - Script do budowania aplikacji
"""
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Wyczyść folder dist
if os.path.exists("dist"):
    shutil.rmtree("dist")

# Stwórz tymczasowy plik .spec
SPEC_CONTENT = '''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icons/*.png', 'assets/icons'),
        ('assets/fonts/*.ttf', 'assets/fonts')
    ],
    hiddenimports=['customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ForestModManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app.ico'
)
'''

with open('forest_mod_manager.spec', 'w', encoding='utf-8') as f:
    f.write(SPEC_CONTENT)

# Uruchom PyInstaller z plikiem .spec
PyInstaller.__main__.run([
    'forest_mod_manager.spec',
    '--clean'
])

# Usuń tymczasowy plik .spec
os.remove('forest_mod_manager.spec')

print("✨ Build completed! Executable is in the 'dist' folder.")