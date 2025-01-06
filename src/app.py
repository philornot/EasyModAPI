"""
src/app.py - Punkt wejściowy aplikacji
"""
import sys
import os
from pathlib import Path
import customtkinter as ctk
from ui.main_window import MainWindow


def get_asset_path(relative_path):
    """Zwraca właściwą ścieżkę do zasobów, działającą zarówno w trybie dev jak i w .exe"""
    if getattr(sys, 'frozen', False):
        # Jesteśmy w .exe
        base_path = sys._MEIPASS
    else:
        # Tryb deweloperski
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


def setup_appearance():
    """Konfiguracja wyglądu aplikacji"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Załaduj własną czcionkę
    font_path = get_asset_path("assets/fonts/Roboto-Regular.ttf")
    if os.path.exists(font_path):
        ctk.FontManager.load_font(font_path)


def main():
    setup_appearance()
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()