"""
build.py - Script do budowania aplikacji
"""
import os
import shutil
from pathlib import Path

import PyInstaller.__main__
import tkinterdnd2

from src.logger import setup_logger

logger = setup_logger("ForestModManagerBuild")


def get_tkdnd_path():
    """Znajduje ścieżkę do biblioteki tkdnd"""
    tkdnd_path = Path(tkinterdnd2.__file__).parent / 'tkdnd'
    logger.info(f"Found tkdnd path: {tkdnd_path}")
    return tkdnd_path


def clean_dist():
    if os.path.exists("dist"):
        logger.info("Cleaning dist directory")
        shutil.rmtree("dist")


def create_spec():
    logger.info("Creating .spec file")
    tkdnd_path = get_tkdnd_path()

    SPEC_CONTENT = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icons/*.png', 'assets/icons'),
        ('assets/fonts/*.ttf', 'assets/fonts'),
        ('src/ui', 'src/ui'),
        ('src/__init__.py', 'src'),
        (r'{tkdnd_path}', 'tkinterdnd2/tkdnd'),
    ],
    hiddenimports=['customtkinter', 'src.ui', 'tkinterdnd2'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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


def build():
    try:
        logger.info("Starting build process")
        clean_dist()
        create_spec()

        logger.info("Running PyInstaller")
        PyInstaller.__main__.run([
            'forest_mod_manager.spec',
            '--clean'
        ])

        logger.info("Cleaning up .spec file")
        os.remove('forest_mod_manager.spec')

        logger.info("✨ Build completed successfully!")
    except Exception as e:
        logger.error(f"Build failed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    build()
