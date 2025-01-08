import os
import shutil
import subprocess
import sys

from src.config import CURRENT_VERSION

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def get_assets_path():
    """Get the path to the assets directory."""
    return os.path.join(project_root, 'assets')


def clean_build_artifacts():
    """Remove previous build and dist directories."""
    for dir_name in ['build', 'dist']:
        full_path = os.path.join(project_root, dir_name)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)


def create_executable():
    """Create a single executable for Forest Mod Manager."""
    print(f"Creating executable for Forest Mod Manager v{CURRENT_VERSION}")

    # Construct PyInstaller arguments
    pyinstaller_args = [
        'pyinstaller',
        '--name', f'ForestModManager-v{CURRENT_VERSION}',
        '--onefile',  # Single executable
        '--windowed',  # No console window
        '--add-data', f'{get_assets_path()}:assets',  # Include assets
        '--icon', os.path.join(get_assets_path(), 'icons', 'app.ico'),  # Application icon
        '--add-data', 'locales:locales',  # Include translation files
        '--hidden-import', 'tkinter',  # Explicitly include Tkinter
        '--hidden-import', 'customtkinter',  # Explicitly include CustomTkinter
        '--hidden-import', 'PIL',  # Explicitly include Pillow
        '--collect-data', 'tkinterdnd2',  # Collect tkinterdnd2 data
        'src/app.py'  # Main entry point
    ]

    # Use subprocess to run PyInstaller
    try:
        subprocess.run(pyinstaller_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)


def main():
    # Ensure we're running from the project root
    os.chdir(project_root)

    # Clean previous builds
    clean_build_artifacts()

    # Create the executable
    create_executable()

    # Print success message with executable location
    print("\n🎉 Build completed successfully!")
    print(f"Executable created: {os.path.join(project_root, 'dist', f'ForestModManager-v{CURRENT_VERSION}.exe')}")


if __name__ == '__main__':
    main()
