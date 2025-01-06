"""
build.py - Script do budowania aplikacji
"""
import os
import shutil
import uuid
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


def create_spec(temp_name):
    """Tworzy plik .spec z tymczasową nazwą pliku wynikowego"""
    logger.info("Creating .spec file")
    tkdnd_path = get_tkdnd_path()
    temp_dist = str(Path("build") / "temp_dist")
    icon_path = os.path.abspath('assets/icons/app.ico')

    SPEC_CONTENT = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icons/*', 'assets/icons'),  # Include all icon files
        ('assets/fonts/*.ttf', 'assets/fonts'),
        ('src/ui', 'src/ui'),
        ('src/__init__.py', 'src'),
        (r'{tkdnd_path}', 'tkinterdnd2/tkdnd'),
    ],
    hiddenimports=['customtkinter', 'src.ui', 'tkinterdnd2', 'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder'],
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
    name='{temp_name}',
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
    icon=r'{icon_path}',
    distpath=r'{temp_dist}'
)
'''
    spec_path = 'forest_mod_manager.spec'
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(SPEC_CONTENT)
    return spec_path


def build():
    try:
        logger.info("Starting build process")

        # Generuj unikalną nazwę dla pliku tymczasowego
        temp_name = f"temp_build_{uuid.uuid4().hex[:8]}"
        logger.debug(f"Using temporary name: {temp_name}")

        # Stwórz .spec z tymczasową nazwą
        spec_file = create_spec(temp_name)

        logger.info("Running PyInstaller")
        PyInstaller.__main__.run([
            spec_file,
            '--clean'
        ])

        # Sprawdź gdzie jest plik
        logger.info("Looking for output file...")

        # Sprawdź różne możliwe lokalizacje
        possible_locations = [
            Path("build") / "temp_dist" / f"{temp_name}.exe",
            Path("temp_dist") / f"{temp_name}.exe",
            Path("dist") / f"{temp_name}.exe",
        ]

        for path in possible_locations:
            logger.info(f"Checking {path}...")
            if path.exists():
                logger.info(f"Found at: {path}")
                temp_exe = path
                break
        else:
            logger.error("Output file not found in any expected location!")
            logger.info("Directory contents:")
            for dir_path in [Path("build"), Path("dist"), Path("temp_dist")]:
                if dir_path.exists():
                    logger.info(f"\nContents of {dir_path}:")
                    for item in dir_path.rglob("*"):
                        logger.info(f"  {item}")
            raise FileNotFoundError("Could not find output file!")

        # Przenieś do docelowej lokalizacji
        target_path = Path("dist")
        target_path.mkdir(exist_ok=True)
        target_exe = target_path / "ForestModManager.exe"

        # Spróbuj usunąć istniejący plik
        if target_exe.exists():
            try:
                logger.info(f"Removing existing file: {target_exe}")
                target_exe.unlink()
            except PermissionError:
                logger.warning("Could not remove existing file - waiting 5 seconds and retrying")
                import time
                time.sleep(5)
                try:
                    target_exe.unlink()
                except Exception as e:
                    logger.error(f"Failed to remove file after retry: {e}")
                    raise

        logger.info(f"Moving {temp_exe} to {target_exe}")
        shutil.move(str(temp_exe), str(target_exe))

        # Posprzątaj
        logger.info("Cleaning up")
        if os.path.exists(spec_file):
            os.remove(spec_file)
        temp_dist = Path("build") / "temp_dist"
        if temp_dist.exists():
            shutil.rmtree(temp_dist)

        logger.info("✨ Build completed successfully!")

    except Exception as e:
        logger.error(f"Build failed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    build()
