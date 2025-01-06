"""
src/ui/main_window.py
"""
import os
import subprocess
import sys
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

from .components import (
    Card, GradientButton, SecondaryButton,
    Title, Subtitle, StatusLabel, IconButton,
    FileDropZone
)
from .styles import Colors
from ..config import Config
from ..installer import ModInstaller
from ..logger import setup_logger

logger = setup_logger("MainWindow")


def get_logs_dir():
    return Path.home() / '.forest_mod_manager' / 'logs'


def get_latest_log():
    logs_dir = get_logs_dir()
    log_files = list(logs_dir.glob("*.log"))
    if log_files:
        return max(log_files, key=lambda x: x.stat().st_mtime)
    return None


def open_file_explorer(path, select_file=None):
    path = Path(path)
    logger.debug(f"Opening file explorer: path={path}, select_file={select_file}")

    try:
        if sys.platform == 'win32':
            if select_file:
                logger.debug("Using Windows explorer with file selection")
                subprocess.run(['explorer', '/select,', str(select_file)])
            else:
                logger.debug("Using Windows startfile")
                os.startfile(path)
        elif sys.platform == 'darwin':
            logger.debug("Using macOS open command")
            if select_file:
                subprocess.run(['open', '-R', str(select_file)])
            else:
                subprocess.run(['open', str(path)])
        else:
            logger.debug("Using Linux xdg-open")
            subprocess.run(['xdg-open', str(path)])
    except Exception as e:
        logger.error(f"Failed to open file explorer: {e}", exc_info=True)


class MainWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        logger.info("Initializing main window")
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        logger.debug(f"TkinterDnD version: {self.TkdndVersion}")

        self.config = Config()
        self.title("The Forest Mod Manager")
        self.geometry("600x500")

        self._setup_window()
        self._create_widgets()

        if self.config.modapi_path:
            logger.info(f"Found existing MODAPI path: {self.config.modapi_path}")
            self.drop_zone.activate()
            self._update_status()
        else:
            logger.info("No MODAPI path configured")
            self.drop_zone.deactivate()

    def _setup_window(self):
        logger.debug("Setting up window properties")
        self.configure(fg_color=Colors.BACKGROUND)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        try:
            from ctypes import windll, c_int, byref, sizeof
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_MICA_EFFECT = 1029

            logger.debug("Applying Windows 11 visual effects")
            windll.dwmapi.DwmSetWindowAttribute(
                self.winfo_id(),
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                byref(c_int(1)),
                sizeof(c_int)
            )
            windll.dwmapi.DwmSetWindowAttribute(
                self.winfo_id(),
                DWMWA_MICA_EFFECT,
                byref(c_int(1)),
                sizeof(c_int)
            )
            logger.debug("Windows 11 effects applied successfully")
        except Exception as e:
            logger.warning(f"Failed to apply Windows 11 effects: {e}")

    def _create_widgets(self):
        logger.debug("Creating widgets")

        # Header
        header = Card(self)
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(pady=10, fill="x")
        header_content.grid_columnconfigure(1, weight=1)

        Title(header_content, text="The Forest Mod Manager").grid(row=0, column=1, pady=(0, 5))
        Subtitle(
            header_content,
            text="Łatwa instalacja modów"
        ).grid(row=1, column=1)

        logs_button = IconButton(
            header_content,
            text="📋",
            tooltip_text="Otwórz folder z logami",
            command=self._open_logs_folder
        )
        logs_button.grid(row=0, column=2, rowspan=2, padx=10)

        # Content
        content = Card(self)
        content.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        self.status_label = StatusLabel(content)
        self.status_label.grid(row=0, column=0, pady=20, padx=20)

        self.drop_zone = FileDropZone(
            content,
            on_file_drop=self._handle_zip,
            height=200
        )
        self.drop_zone.grid(
            row=1, column=0,
            padx=20, pady=(0, 20),
            sticky="nsew"
        )

        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(0, 20))

        GradientButton(
            button_frame,
            text="Wybierz folder MODAPI",
            command=self._select_modapi_folder
        ).pack(side="left", padx=5)

        SecondaryButton(
            button_frame,
            text="Otwórz folder modów",
            command=self._open_mods_folder
        ).pack(side="left", padx=5)

    def _select_modapi_folder(self):
        """Wybór głównego folderu MODAPI."""
        logger.info("Opening MODAPI folder selection dialog")
        folder = filedialog.askdirectory(
            title="Wybierz główny folder MODAPI"
        )
        if folder:
            logger.info(f"Selected MODAPI folder: {folder}")
            installer = ModInstaller(folder)

            if not installer.verify_paths():
                logger.warning("Invalid MODAPI folder structure")
                self.status_label.set_error(
                    "Nieprawidłowy folder!\nWybierz główny folder MODAPI."
                )
                return

            self.config.modapi_path = folder
            self._update_status()
            self.drop_zone.activate()
        else:
            logger.debug("MODAPI folder selection cancelled")

    def _update_status(self):
        path = Path(self.config.modapi_path)
        logger.debug(f"Updating status with path: {path}")
        self.status_label.set_success(
            f"✓ Folder MODAPI:\n{path.name}"
        )

    def _handle_zip(self, zip_path):
        logger.info(f"Handling ZIP file: {zip_path}")
        if not self.config.modapi_path:
            logger.warning("No MODAPI path configured")
            self.status_label.set_error(
                "Najpierw wybierz folder MODAPI!"
            )
            return

        try:
            logger.info("Starting mod installation")
            installer = ModInstaller(self.config.modapi_path)
            installer.install_mods(zip_path)
            logger.info("Mods installed successfully")

            self.status_label.set_success(
                "✓ Mody zainstalowane pomyślnie!"
            )

        except Exception as e:
            logger.error(f"Failed to install mods: {e}", exc_info=True)
            self.status_label.set_error(f"Błąd: {str(e)}")

    def _open_mods_folder(self):
        """Otwiera folder mods/TheForest."""
        if not self.config.modapi_path:
            logger.warning("Cannot open mods folder - no MODAPI path configured")
            self.status_label.set_error(
                "Najpierw wybierz folder MODAPI!"
            )
            return

        installer = ModInstaller(self.config.modapi_path)
        mods_path = installer.mods_path

        if mods_path.exists():
            logger.info(f"Opening mods folder: {mods_path}")
            open_file_explorer(mods_path)
        else:
            logger.error(f"Mods folder does not exist: {mods_path}")
            self.status_label.set_error(
                "Folder mods/TheForest nie istnieje!"
            )

    def _open_logs_folder(self):
        logger.info("Opening logs folder")
        logs_dir = get_logs_dir()
        latest_log = get_latest_log()

        if logs_dir.exists():
            if latest_log:
                logger.debug(f"Opening logs folder with latest log selected: {latest_log}")
                open_file_explorer(logs_dir, latest_log)
            else:
                logger.debug("Opening logs folder (no logs present)")
                open_file_explorer(logs_dir)
