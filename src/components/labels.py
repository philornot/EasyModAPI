import customtkinter as ctk

from .ui.styles import Colors, Styles
from ..logger import setup_logger

logger = setup_logger()


class Title(ctk.CTkLabel):
    """Główny tytuł"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.TITLE.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)
        logger.debug(f"Created Title with kwargs: {kwargs}")


class Subtitle(ctk.CTkLabel):
    """Podtytuł"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.SUBTITLE.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)
        logger.debug(f"Created Subtitle with kwargs: {kwargs}")


class StatusLabel(ctk.CTkLabel):
    """Label do wyświetlania statusu"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.LABEL.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)
        logger.debug(f"Created StatusLabel with kwargs: {kwargs}")

    def set_success(self, text):
        logger.debug(f"Setting success status: {text}")
        self.configure(text=text, text_color=Colors.SUCCESS)

    def set_error(self, text):
        logger.debug(f"Setting error status: {text}")
        self.configure(text=text, text_color=Colors.ERROR)

    def set_warning(self, text):
        logger.debug(f"Setting warning status: {text}")
        self.configure(text=text, text_color=Colors.WARNING)
