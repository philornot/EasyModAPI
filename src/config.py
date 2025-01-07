"""
src/config.py - Konfiguracja aplikacji
"""
import json
import shutil
from pathlib import Path

from .logger import setup_logger

logger = setup_logger("Config")

CONFIG_FILE = Path.home() / '.forest_mod_manager.json'
MODS_DIR = Path.home() / '.forest_mod_manager' / 'mods'
CURRENT_VERSION = "0.6.9"  # Aktualna wersja programu


class Config:
    DEFAULT_CONFIG = {
        'modapi_path': None,
        'saved_mods': [],
        'language': 'en',
        'tutorial_shown': False,
        'last_update_check': None,
        'egg_chance': 10  # 10% szans domyślnie
        # dla testów egg_chance można zwiększyć w init w main_window
    }

    def __init__(self):
        self.config = self._load_config()
        self._ensure_mods_dir()

    def _load_config(self) -> dict:
        """Wczytuje lub tworzy konfigurację"""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}", exc_info=True)

        # Jeśli nie udało się wczytać, użyj domyślnej
        logger.info("Using default configuration")
        return self.DEFAULT_CONFIG.copy()

    def save(self):
        """Zapisuje konfigurację"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save config: {e}", exc_info=True)

    def _ensure_mods_dir(self):
        """Tworzy folder na mody jeśli nie istnieje"""
        try:
            MODS_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Mods directory ensured: {MODS_DIR}")
        except Exception as e:
            logger.error(f"Failed to create mods directory: {e}", exc_info=True)

    @property
    def modapi_path(self) -> str:
        """Ścieżka do folderu MODAPI"""
        return self.config.get('modapi_path')

    @modapi_path.setter
    def modapi_path(self, path: str):
        self.config['modapi_path'] = path
        self.save()

    def get_saved_mods(self) -> list:
        """Zwraca listę zapisanych modów"""
        return self.config.get('saved_mods', [])

    def save_mod_file(self, original_path: Path) -> Path:
        """
        Kopiuje plik moda do folderu mods i zapisuje w konfiguracji.
        Zwraca ścieżkę do zapisanego pliku.
        """
        try:
            # Przygotuj ścieżkę docelową
            target_path = MODS_DIR / original_path.name

            # Skopiuj plik
            shutil.copy2(original_path, target_path)
            logger.info(f"Copied mod file to: {target_path}")

            # Dodaj do listy zapisanych
            saved_mods = self.get_saved_mods()
            mod_info = {'filename': target_path.name}

            if mod_info not in saved_mods:
                saved_mods.append(mod_info)
                self.config['saved_mods'] = saved_mods
                self.save()

            return target_path

        except Exception as e:
            logger.error(f"Failed to save mod file: {e}", exc_info=True)
            raise

    def remove_mod_file(self, filename: str):
        """Usuwa mod z konfiguracji i z dysku"""
        try:
            # Usuń z konfiguracji
            saved_mods = self.get_saved_mods()
            self.config['saved_mods'] = [m for m in saved_mods if m['filename'] != filename]
            self.save()

            # Usuń plik
            mod_path = MODS_DIR / filename
            if mod_path.exists():
                mod_path.unlink()
                logger.info(f"Removed mod file: {filename}")

        except Exception as e:
            logger.error(f"Failed to remove mod file: {e}", exc_info=True)

    def was_tutorial_shown(self) -> bool:
        """Sprawdza czy tutorial był pokazany"""
        return self.config.get('tutorial_shown', False)

    def set_tutorial_shown(self, shown: bool):
        """Zapisuje informację o pokazaniu tutoriala"""
        self.config['tutorial_shown'] = shown
        self.save()

    def get_last_update_check(self) -> str:
        """Pobiera datę ostatniego sprawdzenia aktualizacji"""
        return self.config.get('last_update_check')

    def set_last_update_check(self, date: str):
        """Zapisuje datę sprawdzenia aktualizacji"""
        self.config['last_update_check'] = date
        self.save()

    @property
    def language(self) -> str:
        """Get current language"""
        return self.config.get('language', 'en')

    @language.setter
    def language(self, lang_code: str):
        """Set and save language"""
        self.config['language'] = lang_code
        self.save()

    def get_egg_chance(self) -> float:
        return self.config.get('egg_chance', 10) / 100

    def set_egg_chance(self, chance: int):
        """Ustawia szansę na pojawienie się easter egga (0-100)"""
        self.config['egg_chance'] = max(0, min(100, chance))  # Ograniczenie do zakresu 0-100
        self.save()
