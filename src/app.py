"""
src/app.py - Punkt wejściowy aplikacji
"""
import os
import sys

import customtkinter as ctk

from src.logger import setup_logger
from src.ui.main_window import MainWindow

logger = setup_logger()


def get_asset_path(relative_path):
    """Zwraca właściwą ścieżkę do zasobów, działającą zarówno w trybie dev jak i w .exe"""
    if getattr(sys, 'frozen', False):
        logger.debug(f"Running in exe mode. Base path: {sys._MEIPASS}")
        base_path = sys._MEIPASS
    else:
        logger.debug("Running in dev mode")
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    full_path = os.path.join(base_path, relative_path)
    logger.debug(f"Asset path resolved: {full_path}")
    return full_path


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
