"""
src/ui/components/help_button.py - Help button component
"""
import customtkinter as ctk
from src.components.ui.styles import Colors


class HelpButton(ctk.CTkButton):
    """Help button positioned in the bottom right corner"""

    def __init__(self, master, command):
        super().__init__(
            master,
            text="?",
            width=32,
            height=32,
            corner_radius=16,
            font=("Roboto", 14, "bold"),
            command=command,
            fg_color=Colors.PRIMARY,
            hover_color=Colors.PRIMARY_HOVER
        )

        # Position in bottom right corner
        self.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")