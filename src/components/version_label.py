"""
src/ui/components/version_label.py - Version label component with update check
"""
import webbrowser
from datetime import datetime, timedelta

import customtkinter as ctk

from src.components.ui.styles import Colors
from src.config import CURRENT_VERSION
from src.i18n import _
from src.logger import setup_logger
from src.update_checker import check_for_updates, GITHUB_RELEASE_URL

logger = setup_logger("VersionLabel")


class VersionLabel(ctk.CTkFrame):
    """Version label with update notification"""

    def __init__(self, master, config):
        super().__init__(master, fg_color="transparent")
        self.config = config

        # Version label
        self.version_text = ctk.CTkLabel(
            self,
            text=f"v{CURRENT_VERSION}",
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        )
        self.version_text.pack(side="left", padx=2)

        # Hidden update button
        self.update_button = ctk.CTkButton(
            self,
            text=_("New version available!"),
            command=self._open_release_page,
            font=("Roboto", 11),
            height=24,
            fg_color=Colors.SUCCESS,
            hover_color="#1a7f37"  # Darker shade of green
        )

        # Position at bottom center
        self.place(relx=0.5, rely=1.0, y=-10, anchor="s")

    def check_updates(self):
        """Check for updates if enough time has passed"""
        last_check = self.config.get_last_update_check()

        # Check if 24h passed since last check
        if (not last_check or
                datetime.fromisoformat(last_check) < datetime.now() - timedelta(days=1)):
            logger.debug("Checking for updates")
            new_version = check_for_updates()
            if new_version:
                logger.info(f"New version found: {new_version}")
                self.show_update_button(new_version)

            self.config.set_last_update_check(datetime.now().isoformat())

    def show_update_button(self, new_version: str):
        """Show update button"""
        logger.debug(f"Showing update button for version {new_version}")
        self.version_text.pack_forget()
        self.update_button.configure(
            text=_("Update to {version} available!").format(version=new_version)
        )
        self.update_button.pack(padx=2)

    def _open_release_page(self):
        """Open releases page"""
        logger.debug(f"Opening release page: {GITHUB_RELEASE_URL}")
        webbrowser.open(GITHUB_RELEASE_URL)
