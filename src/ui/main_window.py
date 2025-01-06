"""
src/ui/main_window.py - Main application window
"""
import os
import subprocess
import sys
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image
from tkinterdnd2 import TkinterDnD

from .components import (
    Card, GradientButton, SecondaryButton,
    Title, Subtitle, StatusLabel, FileDropZone, ModCard
)
from .styles import Colors
from ..config import Config, MODS_DIR
from ..i18n import _, set_language  # Import the translation function
from ..installer import ModInstaller
from ..logger import setup_logger
from ..utils import get_asset_path

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
        self.title(_("The Forest Mod Manager"))
        self.geometry("600x600")

        # Ustaw język z konfiguracji
        set_language(self.config.language)

        self.mod_cards = []

        self._setup_window()
        self._create_widgets()

        if self.config.modapi_path:
            logger.info(f"Found existing MODAPI path: {self.config.modapi_path}")
            self.drop_zone.activate()
            self._update_status()
            self._load_saved_mods()
        else:
            logger.info("No MODAPI path configured")
            self.drop_zone.deactivate()

    def _setup_window(self):
        self.configure(fg_color=Colors.BACKGROUND)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        try:
            icon_path = get_asset_path("assets/icons/app.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
                icon_image = Image.open(icon_path)
                # it works so...
                # noinspection PyTypeChecker, PyProtectedMember
                self.wm_iconphoto(True, ctk.CTkImage(
                    light_image=icon_image,
                    dark_image=icon_image,
                    size=(32, 32))._light_image)
        except Exception as e:
            logger.warning(f"Failed to set window icon: {e}", exc_info=True)

    def _create_widgets(self):
        logger.debug("Creating widgets")

        # Header
        header = Card(self)
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(pady=10, fill="x", expand=True)

        # Title column
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(expand=True)

        Title(title_frame, text=_("The Forest Mod Manager")).pack(pady=(0, 5))
        Subtitle(
            title_frame,
            text=_("Easy mod installation")
        ).pack()

        # Przyciski w prawym górnym rogu
        buttons_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        buttons_frame.place(relx=1.0, rely=0.5, anchor="e", x=-30)

        logs_button = SecondaryButton(
            buttons_frame,
            text=_("logs"),
            command=self._open_logs_folder,
            font=("Roboto", 11),
            width=50,
            height=24,
            corner_radius=6
        )
        logs_button.pack(pady=2)

        lang_button = SecondaryButton(
            buttons_frame,
            text="polski" if self.config.language == "en" else "english",
            command=self._toggle_language,
            font=("Roboto", 11),
            width=50,
            height=24,
            corner_radius=6
        )
        lang_button.pack(pady=2)

        # Content
        content = Card(self)
        content.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        self.status_label = StatusLabel(content)
        self.status_label.grid(row=0, column=0, pady=20, padx=20)

        # Scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(
            content,
            fg_color="transparent",
            height=200
        )
        self.scrollable_frame.grid(
            row=1, column=0,
            padx=20, pady=(0, 20),
            sticky="nsew"
        )

        # Drop zone
        self.drop_zone = FileDropZone(
            self.scrollable_frame,
            on_file_drop=self._handle_zip,
            height=120
        )
        self.drop_zone.pack(fill="x", expand=True)

        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(0, 20))

        GradientButton(
            button_frame,
            text=_("Select MODAPI folder"),
            command=self._select_modapi_folder
        ).pack(side="left", padx=5)

        SecondaryButton(
            button_frame,
            text=_("Open mods folder"),
            command=self._open_mods_folder
        ).pack(side="left", padx=5)

    def _select_modapi_folder(self):
        logger.info("Opening MODAPI folder selection dialog")
        folder = filedialog.askdirectory(
            title=_("Select MODAPI main folder")
        )
        if folder:
            logger.info(f"Selected MODAPI folder: {folder}")
            installer = ModInstaller(folder)

            if not installer.verify_paths():
                logger.warning("Invalid MODAPI folder structure")
                self.status_label.set_error(
                    _("Invalid folder!\nSelect MODAPI main folder.")
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
            _("✓ MODAPI Folder:\n{folder_name}").format(folder_name=path.name)
        )

    def _load_saved_mods(self):
        logger.info("Loading saved mods")
        for mod_info in self.config.get_saved_mods():
            mod_path = MODS_DIR / mod_info['filename']
            if mod_path.exists():
                self._add_mod_card(mod_path)
            else:
                logger.warning(f"Mod file not found: {mod_path}")
                self.config.remove_mod_file(mod_info['filename'])

    def _add_mod_card(self, zip_path):
        try:
            mod_card = ModCard(
                self.scrollable_frame,
                zip_path,
                on_install=self._install_mods,
                on_remove=self._remove_mod_card
            )
            mod_card.pack(fill="x", padx=3, pady=2)
            self.mod_cards.append(mod_card)
            return mod_card
        except Exception as e:
            logger.error(f"Failed to create mod card: {e}", exc_info=True)
            return None

    def _handle_zip(self, zip_path):
        logger.info(f"Handling ZIP file: {zip_path}")
        if not self.config.modapi_path:
            logger.warning("No MODAPI path configured")
            self.status_label.set_error(
                _("Select MODAPI folder first!")
            )
            return

        try:
            saved_path = self.config.save_mod_file(zip_path)

            if self._add_mod_card(saved_path):
                self.status_label.set_success(_("✓ ZIP file has been added!"))
            else:
                raise Exception(_("Failed to create mod card"))

        except Exception as e:
            logger.error(f"Failed to handle ZIP file: {e}", exc_info=True)
            self.status_label.set_error(_("Error: {error}").format(error=str(e)))

    def _install_mods(self, zip_path):
        try:
            logger.info("Starting mod installation")
            installer = ModInstaller(self.config.modapi_path)
            installer.install_mods(zip_path)
            logger.info("Mods installed successfully")

            self.status_label.set_success(
                _("✓ Mods installed successfully!")
            )

        except Exception as e:
            logger.error(f"Failed to install mods: {e}", exc_info=True)
            self.status_label.set_error(_("Error: {error}").format(error=str(e)))

    def _remove_mod_card(self, mod_card):
        logger.info(f"Removing mod card and file for: {mod_card.zip_path}")
        self.config.remove_mod_file(mod_card.zip_path.name)
        mod_card.destroy()
        self.mod_cards.remove(mod_card)

    def _open_mods_folder(self):
        if not self.config.modapi_path:
            logger.warning("Cannot open mods folder - no MODAPI path configured")
            self.status_label.set_error(
                _("Select MODAPI folder first!")
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
                _("Folder mods/TheForest does not exist!")
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

    def _toggle_language(self):
        """Toggle between Polish and English"""
        new_lang = "pl" if self.config.language == "en" else "en"
        self.config.language = new_lang
        set_language(new_lang)

        # Odśwież wszystkie teksty w aplikacji
        self.title(_("The Forest Mod Manager"))
        self._update_status()

        # Znajdź i zaktualizuj przycisk języka
        for widget in self.winfo_children():
            if isinstance(widget, Card):  # To jest header
                for content in widget.winfo_children():
                    if isinstance(content, ctk.CTkFrame):  # To jest header_content
                        for frame in content.winfo_children():
                            if isinstance(frame, ctk.CTkFrame):  # To może być logs_button_frame
                                for button in frame.winfo_children():
                                    if isinstance(button, SecondaryButton):
                                        if button.cget("text") in ["polski", "english"]:
                                            button.configure(
                                                text="polski" if new_lang == "en" else "english"
                                            )

        # Odśwież wszystkie teksty w UI
        self.drop_zone.label.configure(
            text=_("Drop ZIP file with mods here\nor click to select")
        )

        # Odśwież przyciski
        for widget in self.winfo_children():
            if isinstance(widget, Card):  # To jest content
                for frame in widget.winfo_children():
                    if isinstance(frame, ctk.CTkFrame) and frame.winfo_children():
                        for button_frame in frame.winfo_children():
                            if isinstance(button_frame, ctk.CTkFrame):
                                for button in button_frame.winfo_children():
                                    if isinstance(button, GradientButton):
                                        if "MODAPI" in button.cget("text"):
                                            button.configure(text=_("Select MODAPI folder"))
                                    elif isinstance(button, SecondaryButton):
                                        if "folder" in button.cget("text"):
                                            button.configure(text=_("Open mods folder"))
