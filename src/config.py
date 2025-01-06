"""
src/config.py - Configuration management
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

CONFIG_FILE = Path.home() / '.forest_mod_manager.json'
MODS_DIR = Path.home() / '.forest_mod_manager' / 'mods'


class Config:
    DEFAULT_CONFIG = {
        'modapi_path': None,
        'saved_mods': [],
        'language': 'en'  # Default language
    }

    def __init__(self):
        self.config = self._load_config()
        self._ensure_mods_dir()

    @property
    def language(self):
        """Get current language"""
        return self.config.get('language', 'en')

    @language.setter
    def language(self, lang_code):
        """Set and save language"""
        self.config['language'] = lang_code
        self.save()

    def _load_config(self):
        """Ładuje konfigurację z pliku lub tworzy domyślną"""
        config = self.DEFAULT_CONFIG.copy()

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Aktualizuj domyślną konfigurację zachowanymi wartościami
                    config.update(saved_config)
            except Exception as e:
                print(f"Error loading config: {e}")

        return config

    def _ensure_mods_dir(self):
        """Tworzy folder na mody jeśli nie istnieje"""
        MODS_DIR.mkdir(parents=True, exist_ok=True)

    def save(self):
        """Zapisuje konfigurację do pliku"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    @property
    def modapi_path(self):
        """Ścieżka do folderu z modami MODAPI"""
        return self.config.get('modapi_path')

    @modapi_path.setter
    def modapi_path(self, path):
        """Ustawia i zapisuje ścieżkę do folderu z modami"""
        if path:
            path = os.path.normpath(path)
        self.config['modapi_path'] = path
        self.save()

    def save_mod_file(self, source_path):
        """
        Kopiuje plik ZIP do folderu mods i dodaje wpis w konfiguracji

        Args:
            source_path (str|Path): Ścieżka do oryginalnego pliku ZIP

        Returns:
            Path: Ścieżka do zapisanego pliku
        """
        source_path = Path(source_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{source_path.name}"
        target_path = MODS_DIR / new_filename

        # Kopiuj plik
        shutil.copy2(source_path, target_path)

        # Upewnij się, że lista modów istnieje
        if 'saved_mods' not in self.config:
            self.config['saved_mods'] = []

        # Dodaj wpis w konfiguracji
        mod_info = {
            'filename': new_filename,
            'original_name': source_path.name,
            'added_at': datetime.now().isoformat()
        }
        self.config['saved_mods'].append(mod_info)
        self.save()

        return target_path

    def remove_mod_file(self, filename):
        """
        Usuwa plik ZIP i jego wpis z konfiguracji

        Args:
            filename (str): Nazwa pliku do usunięcia
        """
        file_path = MODS_DIR / filename
        if file_path.exists():
            file_path.unlink()

        # Upewnij się, że lista modów istnieje
        if 'saved_mods' not in self.config:
            self.config['saved_mods'] = []
            return

        # Usuń wpis z konfiguracji
        self.config['saved_mods'] = [
            mod for mod in self.config['saved_mods']
            if mod['filename'] != filename
        ]
        self.save()

    def get_saved_mods(self):
        """
        Zwraca listę zapisanych modów

        Returns:
            list: Lista słowników z informacjami o modach
        """
        # Upewnij się, że lista modów istnieje
        if 'saved_mods' not in self.config:
            self.config['saved_mods'] = []
            self.save()

        return self.config['saved_mods']
