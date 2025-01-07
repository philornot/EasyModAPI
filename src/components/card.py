import customtkinter as ctk

from src import setup_logger, _
from src.components.ui import Styles

logger = setup_logger()


class Card(ctk.CTkFrame):
    """Karta z tłem i zaokrąglonymi rogami"""

    def __init__(self, *args, **kwargs):
        frame_kwargs = Styles.FRAME.copy()
        frame_kwargs.update(kwargs)
        super().__init__(*args, **frame_kwargs)
        logger.debug(_(f"Created Card with kwargs: {kwargs}"))
