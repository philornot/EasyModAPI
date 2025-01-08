import customtkinter as ctk

from src.components.ui.styles import Styles
from src.logger import setup_logger

logger = setup_logger("Components")


class GradientButton(ctk.CTkButton):
    """Button with gradient and hover effect"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(f"Created GradientButton with kwargs: {kwargs}")


class SecondaryButton(ctk.CTkButton):
    """Secondary (outline) button"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON_SECONDARY.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(f"Created SecondaryButton with kwargs: {kwargs}")


class IconButton(ctk.CTkButton):
    """Button with icon and transparent background"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.ICON_BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug("Created IconButton")