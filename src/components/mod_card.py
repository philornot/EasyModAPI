import zipfile
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from . import Card, GradientButton, SecondaryButton
from .ui.styles import Colors
from .. import _
from ..logger import setup_logger

logger = setup_logger()


class ModCard(Card):
    """Karta wyświetlająca informacje o przesłanym pliku ZIP"""

    def __init__(self, master, zip_path, on_install, on_remove, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.zip_path = Path(zip_path)

        # Frame na zawartość
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=8, pady=4)
        content.grid_columnconfigure(1, weight=1)

        # Nazwa pliku
        ctk.CTkLabel(
            content,
            text=self.zip_path.name,
            font=("Roboto", 13, "bold"),
            text_color=Colors.TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

        # Data dodania i liczba plików w jednym wierszu
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 4))

        # Data dodania
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        ctk.CTkLabel(
            info_frame,
            text=_("Dodano: {}").format(now),
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left", padx=(0, 15))

        # Liczba modów
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                mod_count = len(zip_ref.namelist())
            mod_text = _("Liczba plików: {}").format(mod_count)
        except:
            mod_text = _("Nie można odczytać zawartości ZIP")

        ctk.CTkLabel(
            info_frame,
            text=mod_text,
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left")

        # Przyciski
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        GradientButton(
            button_frame,
            text=_("Zainstaluj"),
            width=90,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_install(self.zip_path)
        ).pack(side="left", padx=(0, 8))

        SecondaryButton(
            button_frame,
            text=_("Usuń"),
            width=70,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_remove(self)
        ).pack(side="left")
