"""
src/config.py - Zarządzanie konfiguracją aplikacji
"""
import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / '.forest_mod_manager.json'


class Config:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        """Ładuje konfigurację z pliku lub tworzy domyślną"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'modapi_path': None}

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