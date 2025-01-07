"""
src/ui/styles.py — Style dla interfejsu użytkownika
"""


class Colors:
    """Paleta kolorów aplikacji"""
    # Główne kolory
    PRIMARY = "#5D3FD3"  # Fioletowy
    PRIMARY_HOVER = "#4930A6"  # Ciemniejszy fiolet
    SECONDARY = "#A682FF"  # Jasny fiolet
    ACCENT = "#FF6B6B"  # Koralowy akcent

    # Tło i karty
    BACKGROUND = "#1A1B26"  # Ciemne tło
    CARD = "#24283B"  # Jaśniejsze tło dla kart
    CARD_HOVER = "#2F354A"  # Hover dla kart

    # Tekst
    TEXT = "#C0CAF5"  # Główny kolor tekstu
    TEXT_SECONDARY = "#9AA5CE"  # Drugorzędny tekst

    # Status
    ERROR = "#F7768E"  # Czerwony dla błędów
    SUCCESS = "#9ECE6A"  # Zielony dla sukcesu
    WARNING = "#E0AF68"  # Pomarańczowy dla ostrzeżeń

    # ?
    EASTER_EGG_TEXT = "#990000"
    EASTER_EGG_OVERLAY = "#FFFFFF"


class Styles:
    """Predefiniowane style dla komponentów"""

    BUTTON = {
        "corner_radius": 10,
        "border_width": 2,
        "fg_color": Colors.PRIMARY,
        "hover_color": Colors.SECONDARY,
        "text_color": Colors.TEXT,
        "font": ("Roboto", 13),
    }

    BUTTON_SECONDARY = {
        **BUTTON,
        "fg_color": "transparent",
        "border_color": Colors.SECONDARY,
        "hover_color": Colors.CARD_HOVER,
    }

    ICON_BUTTON = {
        "corner_radius": 8,
        "width": 30,
        "height": 30,
        "fg_color": "transparent",
        "hover_color": Colors.CARD_HOVER,
        "text_color": Colors.TEXT_SECONDARY,
    }

    FRAME = {
        "corner_radius": 15,
        "fg_color": Colors.CARD,
        "border_width": 2,
        "border_color": Colors.SECONDARY,
    }

    LABEL = {
        "font": ("Roboto", 13),
        "text_color": Colors.TEXT,
    }

    TITLE = {
        "font": ("Roboto", 24, "bold"),
        "text_color": Colors.TEXT,
    }

    SUBTITLE = {
        "font": ("Roboto", 16),
        "text_color": Colors.TEXT_SECONDARY,
    }
