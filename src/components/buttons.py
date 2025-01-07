import customtkinter as ctk

from src import _
from src.components.ui.styles import Styles
from src.logger import setup_logger

logger = setup_logger("Components")


class GradientButton(ctk.CTkButton):
    """Przycisk z gradientem i efektem hover"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(_("Created GradientButton with kwargs: {}").format(kwargs))


class SecondaryButton(ctk.CTkButton):
    """Przycisk drugorzędny (outline)"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON_SECONDARY.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(_("Created SecondaryButton with kwargs: {}").format(kwargs))


class IconButton(ctk.CTkButton):
    """Przycisk z ikoną bez tła"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.ICON_BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(_("Created IconButton"))
