import customtkinter as ctk

from src import setup_logger
from src.components.ui import Styles

logger = setup_logger()


class Card(ctk.CTkFrame):
    """Card with background and rounded corners"""

    def __init__(self, *args, **kwargs):
        frame_kwargs = Styles.FRAME.copy()
        frame_kwargs.update(kwargs)
        super().__init__(*args, **frame_kwargs)
        logger.debug(f"Created Card with kwargs: {kwargs}")
