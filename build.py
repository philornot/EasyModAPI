"""
build.py - Skrypt do budowania aplikacji
"""
import os
import sys
from pathlib import Path

from cx_Freeze import setup, Executable

# Upewnij się, że jesteśmy w głównym katalogu projektu
os.chdir(Path(__file__).parent)

# Pliki do dołączenia
additional_files = [
    ('assets/icons', 'assets/icons'),  # Ikony (w tym deer1.png i deer2.png)
    ('assets/fonts', 'assets/fonts'),  # Czcionki (Indie Flower i Roboto)
    ('locales', 'locales'),  # Tłumaczenia
]

# Zależności
build_exe_options = {
    "packages": [
        "os",
        "tkinter",
        "customtkinter",
        "PIL",
        "logging",
        "webbrowser",
        "random"
    ],
    "includes": [
        "tkinter",
        "tkinterdnd2"
    ],
    "include_files": additional_files,
    "exclude_files": ["__pycache__"],
    "include_msvcr": True,  # Dla Windows
}

# Ikona aplikacji
icon_file = "assets/icons/app.ico" if sys.platform == "win32" else None

# Stwórz executable
setup(
    name="Forest Mod Manager",
    version="0.6.9",
    description="Mod Manager for The Forest",
    author="philornot",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {  # Opcje dla instalatora MSI (Windows)
            "upgrade_code": "{1234567-1234-1234-1234-123456789012}",
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\Forest Mod Manager",
        }
    },
    executables=[
        Executable(
            "src/app.py",
            base="Win32GUI" if sys.platform == "win32" else None,
            icon=icon_file,
            target_name="Forest Mod Manager.exe",
            copyright="Copyright (c) 2025 philornot"
        )
    ]
)


# Post-build cleanup
def cleanup():
    """Usuwa niepotrzebne pliki po buildzie"""
    build_dir = Path("build")
    if build_dir.exists():
        # Usuń pliki .pyc i __pycache__
        for path in build_dir.rglob("*.pyc"):
            path.unlink()
        for path in build_dir.rglob("__pycache__"):
            for file in path.iterdir():
                file.unlink()
            path.rmdir()


if __name__ == "__main__":
    try:
        print("Building Forest Mod Manager...")
        # Tu będzie automatycznie wywołany setup() przez cx_Freeze
        print("Build completed successfully!")
        cleanup()
        print("Cleanup completed!")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)
