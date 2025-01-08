"""
src/ui/styles.py - UI styles and theme configuration
"""


class Colors:
    """Application color palette"""
    # Main colors
    PRIMARY = "#5D3FD3"  # Purple
    PRIMARY_HOVER = "#4930A6"  # Darker purple
    SECONDARY = "#A682FF"  # Light purple
    ACCENT = "#FF6B6B"  # Coral accent

    # Background and cards
    BACKGROUND = "#1A1B26"  # Dark background
    CARD = "#24283B"  # Lighter card background
    CARD_HOVER = "#2F354A"  # Card hover state

    # Text
    TEXT = "#C0CAF5"  # Primary text
    TEXT_SECONDARY = "#9AA5CE"  # Secondary text

    # Status
    ERROR = "#F7768E"  # Red for errors
    SUCCESS = "#9ECE6A"  # Green for success
    WARNING = "#E0AF68"  # Orange for warnings

    # Easter egg
    EASTER_EGG_TEXT = "#990000"
    EASTER_EGG_OVERLAY = "#FFFFFF"


class Styles:
    """Predefined component styles"""

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