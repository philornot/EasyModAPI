"""
src/ui/components/tutorial.py - Simple tutorial components
"""
from typing import Callable

import customtkinter as ctk

from src.components.ui.styles import Colors
from src.i18n import _
from src.logger import setup_logger

logger = setup_logger(__name__)


class TutorialOverlay(ctk.CTkFrame):
    """Semi-transparent overlay for tutorial"""

    class TutorialOverlay(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(
                master,
                fg_color=("#1A1B2630", "#1A1B2630"),  # Bardzo transparentny kolor
                corner_radius=0,
                border_width=0
            )
            self.place(x=0, y=0, relwidth=1, relheight=1)

    @staticmethod
    def highlight_element(element: ctk.CTkBaseClass):
        """Bring highlighted element to front"""
        if element:
            element.lift()


class TutorialBubble(ctk.CTkFrame):
    """Tutorial message bubble"""

    def __init__(self, master, text: str, element: ctk.CTkBaseClass,
                 on_next: Callable, on_previous: Callable = None,
                 is_last: bool = False):
        super().__init__(
            master,
            fg_color=Colors.CARD,
            corner_radius=15
        )

        # Message
        self.message = ctk.CTkLabel(
            self,
            text=text,
            font=("Roboto", 13),
            wraplength=300,
            justify="left",
            text_color=Colors.TEXT
        )
        self.message.pack(padx=20, pady=(20, 10))

        # Buttons
        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(padx=20, pady=(0, 20), fill="x")

        # Previous button
        if on_previous:
            ctk.CTkButton(
                buttons,
                text=_("← Previous"),
                command=on_previous,
                fg_color="transparent",
                border_color=Colors.SECONDARY,
                border_width=2,
                text_color=Colors.TEXT,
                hover_color=Colors.CARD_HOVER,
                width=90,
                height=32
            ).pack(side="left", padx=5)

        # Next/Done button
        ctk.CTkButton(
            buttons,
            text=_("Got it!") if is_last else _("Next →"),
            command=on_next,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER,
            width=90,
            height=32
        ).pack(side="right", padx=5)

        self._position_bubble(element)

    def _position_bubble(self, element):
        """Position bubble near the target element"""
        # Get element position
        x = element.winfo_rootx() - self.master.winfo_rootx()
        y = element.winfo_rooty() - self.master.winfo_rooty()

        # Get dimensions
        element_width = element.winfo_width()
        element_height = element.winfo_height()
        bubble_width = 340  # Fixed width
        bubble_height = 150  # Approximate height

        # Try to position on the right
        bubble_x = x + element_width + 20
        bubble_y = y - (bubble_height - element_height) // 2

        # If too close to right edge, place below
        if bubble_x + bubble_width > self.master.winfo_width() - 20:
            bubble_x = x - (bubble_width - element_width) // 2
            bubble_y = y + element_height + 20

        # Ensure bubble stays within window
        bubble_x = max(20, min(bubble_x, self.master.winfo_width() - bubble_width - 20))
        bubble_y = max(20, min(bubble_y, self.master.winfo_height() - bubble_height - 20))

        self.place(x=bubble_x, y=bubble_y)
