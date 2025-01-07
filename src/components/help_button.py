"""
src/ui/components/help_button.py - Przycisk pomocy
"""
import customtkinter as ctk
from src.components.ui.styles import Colors


class HelpButton(ctk.CTkButton):
    """Przycisk pomocy w prawym dolnym rogu"""

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

        # Pozycjonuj w prawym dolnym rogu
        self.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")