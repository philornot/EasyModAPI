"""
src/installer.py - Logika instalacji modów
"""
import os
import shutil
import zipfile
from pathlib import Path


class ModInstaller:
    def __init__(self, modapi_path):
        self.modapi_path = Path(modapi_path)

    def install_mods(self, zip_path):
        """
        Instaluje mody z pliku ZIP.

        Args:
            zip_path (str): Ścieżka do pliku ZIP z modami

        Raises:
            Exception: Jeśli wystąpi problem podczas instalacji
        """
        if not self.modapi_path.exists():
            raise Exception("Folder MODAPI nie istnieje!")

        if not zipfile.is_zipfile(zip_path):
            raise Exception("Wybrany plik nie jest poprawnym plikiem ZIP!")

        # Wyczyść folder
        self._clear_mods()

        # Rozpakuj nowe mody
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.modapi_path)

    def _clear_mods(self):
        """Usuwa wszystkie pliki z folderu modów."""
        for item in os.listdir(self.modapi_path):
            item_path = self.modapi_path / item
            if item_path.is_file():
                item_path.unlink()
            elif item_path.is_dir():
                shutil.rmtree(item_path)