"""
src/app.py - Application entry point
"""
import os

import customtkinter as ctk

from src.components.ui.main_window import MainWindow
from src.logger import setup_logger
from src.utils import get_asset_path

logger = setup_logger()


def setup_appearance():
    """Configure application appearance"""
    logger.info("Setting up application appearance")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Load fonts
    fonts = [
        "assets/fonts/Roboto/Roboto-Regular.ttf",
        "assets/fonts/IndieFlower-Regular.ttf"
    ]

    for font_path in fonts:
        full_path = get_asset_path(font_path)
        if os.path.exists(full_path):
            logger.debug(f"Loading font: {full_path}")
            ctk.FontManager.load_font(full_path)
        else:
            logger.warning(f"Font not found at: {full_path}")


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