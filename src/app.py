"""
src/app.py - Punkt wejściowy aplikacji
"""
import os

import customtkinter as ctk

from src.logger import setup_logger
from src.ui.main_window import MainWindow
from src.utils import get_asset_path

logger = setup_logger()


def setup_appearance():
    """Konfiguracja wyglądu aplikacji"""
    logger.info("Setting up application appearance")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    font_path = get_asset_path("assets/fonts/Roboto-Regular.ttf")
    if os.path.exists(font_path):
        logger.debug(f"Loading custom font: {font_path}")
        ctk.FontManager.load_font(font_path)
    else:
        logger.warning(f"Custom font not found at: {font_path}")


def main():
    try:
        logger.info("Starting Forest Mod Manager")
        setup_appearance()
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application crashed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
