"""
src/i18n.py - Internationalization system
"""
import gettext
from typing import Optional

from .logger import setup_logger
from .utils import get_asset_path

logger = setup_logger("I18n")


class I18n:
    """Handles application internationalization"""

    def __init__(self):
        self.current_language = "en"  # Default language
        self._translator: Optional[gettext.NullTranslations] = None
        self._init_translations()

    def _init_translations(self):
        """Initialize the translation system"""
        try:
            locale_dir = get_asset_path("locales")
            logger.debug(f"Loading translations from: {locale_dir}")

            self._translator = gettext.translation(
                "forest_mod_manager",
                locale_dir,
                languages=[self.current_language],
                fallback=True
            )
            self._translator.install()

        except Exception as e:
            logger.error(f"Failed to initialize translations: {e}", exc_info=True)
            self._translator = gettext.NullTranslations()

    def set_language(self, language_code: str):
        """
        Change current language

        Args:
            language_code (str): Language code (e.g. 'en', 'pl')
        """
        self.current_language = language_code
        self._init_translations()

    def get_text(self, text: str) -> str:
        """
        Get translated text

        Args:
            text (str): Text to translate

        Returns:
            str: Translated text
        """
        return self._translator.gettext(text)


# Global translation instance
_i18n = I18n()


# Shortcut function for translations
def _(text: str) -> str:
    """Shortcut for gettext"""
    return _i18n.get_text(text)


def set_language(language_code: str):
    """Change current language"""
    _i18n.set_language(language_code)
