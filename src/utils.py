"""
src/utils.py - Funkcje pomocnicze
"""
import os
import sys
from src.logger import setup_logger

logger = setup_logger("Utils")

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