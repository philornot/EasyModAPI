"""
src/ui/components/tutorial.py - Tutorial components
"""
from typing import Callable

import customtkinter as ctk

from src.components.ui.styles import Colors, Styles
from src.i18n import _


class TutorialOverlay(ctk.CTkFrame):
    """Semi-transparent overlay with a hole for highlighted element"""

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="rgba(0, 0, 0, 0.5)",
            corner_radius=0
        )
        self.configure(bg_color="transparent")

        self.highlighted_elements = []
        self.place(x=0, y=0, relwidth=1, relheight=1)

    def highlight_element(self, element: ctk.CTkBaseClass):
        """Highlight element by creating a 'hole' in the overlay"""
        self.highlighted_elements = [element]
        self.update()

    def remove_highlight(self):
        """Remove all highlights"""
        self.highlighted_elements = []
        self.update()


class TutorialBubble(ctk.CTkFrame):
    """Information bubble with navigation buttons"""

    def __init__(self, master, text: str, element: ctk.CTkBaseClass,
                 on_next: Callable, on_previous: Callable = None,
                 is_last: bool = False):
        super().__init__(
            master,
            fg_color=Colors.CARD,
            corner_radius=12
        )

        # Arrow pointing to element
        self.arrow = ctk.CTkLabel(
            self,
            text="↑",  # Unicode arrow
            font=("Roboto", 24),
            text_color=Colors.TEXT
        )

        # Message text
        message = ctk.CTkLabel(
            self,
            text=text,
            font=("Roboto", 13),
            wraplength=300,
            justify="left"
        )
        message.pack(padx=20, pady=(20, 10))

        # Navigation buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(padx=20, pady=(0, 20), fill="x")

        if on_previous:
            ctk.CTkButton(
                button_frame,
                text=_("← Previous"),
                width=90,
                command=on_previous,
                **Styles.BUTTON_SECONDARY
            ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text=_("Got it!") if is_last else _("Next →"),
            width=90,
            command=on_next
        ).pack(side="right", padx=5)

        # Position bubble relative to element
        self._position_near_element(element)

    def _position_near_element(self, element):
        """Position bubble next to target element"""
        # Get element coordinates relative to main window
        x = element.winfo_rootx() - self.master.winfo_rootx()
        y = element.winfo_rooty() - self.master.winfo_rooty()
        element_width = element.winfo_width()
        element_height = element.winfo_height()

        # Try to place on the right by default
        bubble_x = x + element_width + 10
        bubble_y = y + (element_height - self.winfo_reqheight()) // 2

        # If it doesn't fit on right, try below
        if bubble_x + self.winfo_reqwidth() > self.master.winfo_width():
            bubble_x = x + (element_width - self.winfo_reqwidth()) // 2
            bubble_y = y + element_height + 10
            self.arrow.configure(text="↑")
        else:
            self.arrow.configure(text="←")

        # Ensure bubble stays within window bounds
        bubble_x = max(10, min(bubble_x, self.master.winfo_width() - self.winfo_reqwidth() - 10))
        bubble_y = max(10, min(bubble_y, self.master.winfo_height() - self.winfo_reqheight() - 10))

        self.place(x=bubble_x, y=bubble_y)
