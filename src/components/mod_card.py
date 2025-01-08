"""
src/components/mod_card.py - Mod information card component
"""
import zipfile
from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from src.i18n import _
from src.logger import setup_logger
from . import Card, GradientButton, SecondaryButton
from .ui.styles import Colors

logger = setup_logger()


class ModCard(Card):
    """Card displaying information about uploaded ZIP file"""

    def __init__(self, master, zip_path, on_install, on_remove, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.zip_path = Path(zip_path)
        logger.debug(f"Creating mod card for: {zip_path}")

        # Content frame
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=8, pady=4)
        content.grid_columnconfigure(1, weight=1)

        # File name
        ctk.CTkLabel(
            content,
            text=self.zip_path.name,
            font=("Roboto", 13, "bold"),
            text_color=Colors.TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

        # Info frame for date and file count
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 4))

        # Add date
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        ctk.CTkLabel(
            info_frame,
            text=_("Added: {}").format(now),
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left", padx=(0, 15))

        # File count
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                mod_count = len(zip_ref.namelist())
            logger.debug(f"Found {mod_count} files in ZIP")
            mod_text = _("Files count: {}").format(mod_count)
        except Exception as e:
            logger.error(f"Failed to read ZIP contents: {e}")
            mod_text = _("Cannot read ZIP contents")

        ctk.CTkLabel(
            info_frame,
            text=mod_text,
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left")

        # Buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        GradientButton(
            button_frame,
            text=_("Install"),
            width=90,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_install(self.zip_path)
        ).pack(side="left", padx=(0, 8))

        SecondaryButton(
            button_frame,
            text=_("Remove"),
            width=70,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_remove(self)
        ).pack(side="left")
