"""
src/update_checker.py - Update checking system
"""
import urllib.request
import json
from datetime import datetime, timedelta
import webbrowser
from typing import Optional, Tuple
import customtkinter as ctk

from . import setup_logger
from .components.ui import Colors
from .config import CURRENT_VERSION
from .i18n import _

logger = setup_logger()

GITHUB_API_URL = "https://api.github.com/repos/philornot/EasyModAPI/releases"
GITHUB_RELEASE_URL = "https://github.com/philornot/EasyModAPI/releases"


def parse_version(version: str) -> tuple:
    """Convert version string to tuple for comparison"""
    return tuple(map(int, version.lstrip('v').split('.')))


def check_for_updates() -> Optional[str]:
    """
    Check latest version on GitHub.
    Returns new version number if available, None if not.
    """
    try:
        # Get releases list
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read())

        # Find latest stable release
        current_version = parse_version(CURRENT_VERSION)
        newest_version = None

        for release in releases:
            if not release.get('prerelease', False):  # Ignore prereleases
                version = parse_version(release['tag_name'])
                if version > current_version:
                    if newest_version is None or version > newest_version:
                        newest_version = version

        if newest_version:
            return f"v{'.'.join(map(str, newest_version))}"
        return None

    except Exception as e:
        logger.error(f"Failed to check for updates: {e}")
        return None


class VersionLabel(ctk.CTkFrame):
    """Version label component with update notification"""

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