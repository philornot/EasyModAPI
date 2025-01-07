"""
src/ui/components/tutorial.py - Komponenty tutoriala
"""
from typing import Callable

import customtkinter as ctk

from src.components.ui.styles import Colors, Styles
from src.i18n import _


class TutorialOverlay(ctk.CTkFrame):
    """Półprzezroczysta nakładka z dziurą na podświetlony element"""

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
        """Podświetla element tworząc 'dziurę' w nakładce"""
        self.highlighted_elements = [element]
        self.update()

    def remove_highlight(self):
        """Usuwa wszystkie podświetlenia"""
        self.highlighted_elements = []
        self.update()


class TutorialBubble(ctk.CTkFrame):
    """Dymek z informacją i przyciskami"""

    def __init__(self, master, text: str, element: ctk.CTkBaseClass,
                 on_next: Callable, on_previous: Callable = None,
                 is_last: bool = False):
        super().__init__(
            master,
            fg_color=Colors.CARD,
            corner_radius=12
        )

        # Strzałka wskazująca na element
        self.arrow = ctk.CTkLabel(
            self,
            text="↑",  # Unicode strzałka
            font=("Roboto", 24),
            text_color=Colors.TEXT
        )

        # Tekst
        message = ctk.CTkLabel(
            self,
            text=text,
            font=("Roboto", 13),
            wraplength=300,
            justify="left"
        )
        message.pack(padx=20, pady=(20, 10))

        # Przyciski
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

        # Pozycjonuj dymek względem elementu
        self._position_near_element(element)

    def _position_near_element(self, element):
        """Pozycjonuje dymek obok elementu"""
        # Pobierz współrzędne elementu względem okna głównego
        x = element.winfo_rootx() - self.master.winfo_rootx()
        y = element.winfo_rooty() - self.master.winfo_rooty()
        element_width = element.winfo_width()
        element_height = element.winfo_height()

        # Domyślnie spróbuj umieścić po prawej
        bubble_x = x + element_width + 10
        bubble_y = y + (element_height - self.winfo_reqheight()) // 2

        # Jeśli nie mieści się po prawej, spróbuj pod elementem
        if bubble_x + self.winfo_reqwidth() > self.master.winfo_width():
            bubble_x = x + (element_width - self.winfo_reqwidth()) // 2
            bubble_y = y + element_height + 10
            self.arrow.configure(text="↑")
        else:
            self.arrow.configure(text="←")

        # Upewnij się, że dymek nie wychodzi poza okno
        bubble_x = max(10, min(bubble_x, self.master.winfo_width() - self.winfo_reqwidth() - 10))
        bubble_y = max(10, min(bubble_y, self.master.winfo_height() - self.winfo_reqheight() - 10))

        self.place(x=bubble_x, y=bubble_y)
