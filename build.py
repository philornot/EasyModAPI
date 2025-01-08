"""
build.py - Application build script
"""
import os
import sys
from pathlib import Path

from cx_Freeze import setup, Executable

# Ensure we're in the project root directory
os.chdir(Path(__file__).parent)

# Files to include
additional_files = [
    ('assets/icons', 'assets/icons'),  # Icons (including deer1.png and deer2.png)
    ('assets/fonts', 'assets/fonts'),  # Fonts (Indie Flower and Roboto)
    ('locales', 'locales'),  # Translations
]

# Dependencies
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
    "include_msvcr": True,  # For Windows
}

# Application icon
icon_file = "assets/icons/app.ico" if sys.platform == "win32" else None

# Create executable
setup(
    name="Forest Mod Manager",
    version="0.6.9",
    description="Mod Manager for The Forest",
    author="philornot",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {  # MSI installer options (Windows)
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
    """Remove unnecessary files after build"""
    build_dir = Path("build")
    if build_dir.exists():
        # Remove .pyc files and __pycache__ directories
        for path in build_dir.rglob("*.pyc"):
            path.unlink()
        for path in build_dir.rglob("__pycache__"):
            for file in path.iterdir():
                file.unlink()
            path.rmdir()


if __name__ == "__main__":
    try:
        print("Building Forest Mod Manager...")
        # setup() will be automatically called by cx_Freeze here
        print("Build completed successfully!")
        cleanup()
        print("Cleanup completed!")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)
