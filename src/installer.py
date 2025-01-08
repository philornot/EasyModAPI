"""
src/installer.py - Mod installation logic
"""
import os
import shutil
import zipfile
from pathlib import Path

from src.i18n import _
from src.logger import setup_logger

logger = setup_logger("ModInstaller")


class ModInstaller:
    def __init__(self, modapi_path):
        """
        Args:
            modapi_path (str): Path to main MODAPI folder
        """
        self.modapi_path = Path(modapi_path)
        self.mods_path = self.modapi_path / "mods" / "TheForest"
        logger.debug(f"Initialized ModInstaller with path: {modapi_path}")

    def verify_paths(self):
        """
        Verify if folder structure is correct.

        Returns:
            bool: True if structure is correct, False otherwise
        """
        if not self.modapi_path.exists():
            logger.warning("MODAPI path does not exist")
            return False

        # Check if mods/TheForest path exists
        if not self.mods_path.exists():
            logger.warning("TheForest mods path does not exist")
            return False

        logger.debug("Path verification successful")
        return True

    def install_mods(self, zip_path):
        """
        Install mods from ZIP file.

        Args:
            zip_path (str): Path to ZIP file with mods

        Raises:
            Exception: If installation fails
        """
        if not self.verify_paths():
            error_msg = _("Invalid MODAPI folder structure!\nMake sure you selected the main MODAPI folder.")
            logger.error("Invalid MODAPI folder structure")
            raise Exception(error_msg)

        if not zipfile.is_zipfile(zip_path):
            error_msg = _("Selected file is not a valid ZIP file!")
            logger.error("Invalid ZIP file")
            raise Exception(error_msg)

        # Clear TheForest folder
        self._clear_mods()

        # Extract new mods
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.mods_path)
            logger.info("Mods installed successfully")

    def _clear_mods(self):
        """Remove all files from TheForest folder."""
        logger.debug("Clearing mods folder")
        for item in os.listdir(self.mods_path):
            item_path = self.mods_path / item
            if item_path.is_file():
                item_path.unlink()
                logger.debug(f"Removed file: {item}")
            elif item_path.is_dir():
                shutil.rmtree(item_path)
                logger.debug(f"Removed directory: {item}")
