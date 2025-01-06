"""
src/ui/main_window.py - Główne okno aplikacji
"""
import os
import subprocess
import sys
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from .components import (
    Card, GradientButton, SecondaryButton,
    Title, Subtitle, StatusLabel, IconButton
)
from .styles import Colors
from ..config import Config
from ..installer import ModInstaller


def get_logs_dir():
    """Zwraca ścieżkę do folderu z logami"""
    return Path.home() / '.forest_mod_manager' / 'logs'


def get_latest_log():
    """Zwraca najnowszy plik logu"""
    logs_dir = get_logs_dir()
    log_files = list(logs_dir.glob("*.log"))
    if log_files:
        return max(log_files, key=lambda x: x.stat().st_mtime)
    return None


def open_file_explorer(path, select_file=None):
    """
    Otwiera eksplorator plików w podanej lokalizacji.
    Jeśli podano select_file, próbuje go wybrać.
    """
    if sys.platform == 'win32':
        if select_file:
            # Na Windows używamy explorer z parametrem /select,
            # który podświetli wybrany plik
            subprocess.run(['explorer', '/select,', str(select_file)])
        else:
            os.startfile(path)
    elif sys.platform == 'darwin':  # macOS
        if select_file:
            subprocess.run(['open', '-R', str(select_file)])
        else:
            subprocess.run(['open', str(path)])
    else:  # Linux
        # Na Linux używamy domyślnego menedżera plików
        # Nie ma standardowego sposobu na wybranie pliku
        subprocess.run(['xdg-open', str(path)])


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = Config()

        self.title("The Forest Mod Manager")
        self.geometry("600x500")
        self._setup_window()
        self._create_widgets()

        # Aktywuj/deaktywuj drop zone w zależności od obecności ścieżki
        if self.config.modapi_path:
            self.drop_zone.activate()
            self._update_status()
        else:
            self.drop_zone.deactivate()

    def _setup_window(self):
        """Konfiguracja głównego okna"""
        self.configure(fg_color=Colors.BACKGROUND)

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Efekt szkła (Windows 11)
        try:
            from ctypes import windll, c_int, byref, sizeof
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_MICA_EFFECT = 1029
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
        except:
            pass

    def _create_widgets(self):
        """Tworzenie interfejsu"""
        # Header
        header = Card(self)
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        Title(header, text="The Forest Mod Manager").pack(pady=10)
        Subtitle(
            header,
            text="Łatwa instalacja modów"
        ).pack(pady=(0, 10))

        # Main content
        content = Card(self)
        content.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        # Status
        self.status_label = StatusLabel(content)
        self.status_label.grid(row=0, column=0, pady=20, padx=20)

        # Drop zone
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

        # Buttons container
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

        # Logs button (bottom right corner)
        logs_button = IconButton(
            content,
            text="📋",  # Można zastąpić ikoną
            command=self._open_logs_folder,
            tooltip_text="Otwórz folder z logami"
        )
        logs_button.grid(row=2, column=0, padx=(0, 10), pady=(0, 10), sticky="se")

    def _select_modapi_folder(self):
        """Wybór folderu MODAPI"""
        folder = filedialog.askdirectory(
            title="Wybierz folder MODAPI/mods/TheForest"
        )
        if folder:
            self.config.modapi_path = folder
            self._update_status()
            self.drop_zone.activate()

    def _update_status(self):
        """Aktualizacja statusu"""
        path = Path(self.config.modapi_path)
        self.status_label.set_success(
            f"✓ Folder MODAPI:\n{path.name}"
        )

    def _handle_zip(self, zip_path):
        """Obsługa pliku ZIP z modami"""
        if not self.config.modapi_path:
            self.status_label.set_error(
                "Najpierw wybierz folder MODAPI!"
            )
            return

        try:
            installer = ModInstaller(self.config.modapi_path)
            installer.install_mods(zip_path)

            self.status_label.set_success(
                "✓ Mody zainstalowane pomyślnie!"
            )

        except Exception as e:
            self.status_label.set_error(f"Błąd: {str(e)}")

    def _open_mods_folder(self):
        """Otwiera folder z modami w eksploratorze"""
        if not self.config.modapi_path:
            self.status_label.set_error(
                "Najpierw wybierz folder MODAPI!"
            )
            return

        path = Path(self.config.modapi_path)
        if path.exists():
            open_file_explorer(path)
        else:
            self.status_label.set_error(
                "Folder nie istnieje!"
            )

    def _open_logs_folder(self):
        """Otwiera folder z logami i wybiera najnowszy plik"""
        logs_dir = get_logs_dir()
        latest_log = get_latest_log()

        if logs_dir.exists():
            if latest_log:
                # Otwórz folder z wybranym najnowszym plikiem
                open_file_explorer(logs_dir, latest_log)
            else:
                # Jeśli nie ma plików, po prostu otwórz folder
                open_file_explorer(logs_dir)
