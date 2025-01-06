"""
src/installer.py - Poprawiona logika instalacji modów
"""
import os
import shutil
import zipfile
from pathlib import Path


class ModInstaller:
    def __init__(self, modapi_path):
        """
        Args:
            modapi_path (str): Ścieżka do głównego folderu MODAPI
        """
        self.modapi_path = Path(modapi_path)
        self.mods_path = self.modapi_path / "mods" / "TheForest"

    def verify_paths(self):
        """
        Sprawdza czy struktura folderów jest poprawna.

        Returns:
            bool: True jeśli struktura jest poprawna, False w przeciwnym razie
        """
        if not self.modapi_path.exists():
            return False

        # Sprawdź czy istnieje ścieżka mods/TheForest
        if not self.mods_path.exists():
            return False

        return True

    def install_mods(self, zip_path):
        """
        Instaluje mody z pliku ZIP.

        Args:
            zip_path (str): Ścieżka do pliku ZIP z modami

        Raises:
            Exception: Jeśli wystąpi problem podczas instalacji
        """
        if not self.verify_paths():
            raise Exception("Nieprawidłowa struktura folderów MODAPI!\nUpewnij się że wybrałeś główny folder MODAPI.")

        if not zipfile.is_zipfile(zip_path):
            raise Exception("Wybrany plik nie jest poprawnym plikiem ZIP!")

        # Wyczyść folder TheForest
        self._clear_mods()

        # Rozpakuj nowe mody
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.mods_path)

    def _clear_mods(self):
        """Usuwa wszystkie pliki z folderu TheForest."""
        for item in os.listdir(self.mods_path):
            item_path = self.mods_path / item
            if item_path.is_file():
                item_path.unlink()
            elif item_path.is_dir():
                shutil.rmtree(item_path)