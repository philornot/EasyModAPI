"""
src/ui/tutorial_manager.py - Zarządzanie tutorialem
"""
from dataclasses import dataclass
from typing import Dict, Optional

import customtkinter as ctk

from src import setup_logger
from src.components.tutorial import TutorialOverlay, TutorialBubble
from src.i18n import _

logger = setup_logger()


@dataclass
class TutorialStep:
    """Reprezentuje pojedynczy krok tutoriala"""
    element_id: str  # ID elementu do podświetlenia
    message: str  # Tekst w dymku
    required_action: Optional[str] = None  # Akcja wymagana do przejścia dalej


class Tutorial:
    """Główna klasa tutoriala"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.current_step = 0
        self.overlay: Optional[TutorialOverlay] = None
        self.bubble: Optional[TutorialBubble] = None
        self.element_map: Dict[str, ctk.CTkBaseClass] = {}

        # Zdefiniuj kroki tutoriala
        self.steps = [
            TutorialStep(
                "modapi_button",
                _("Hey there! 👋 Let's get your mods working!\n\nFirst, click the 'Select MODAPI folder' button to tell me where you installed MODAPI."),
                "select_modapi"
            ),
            TutorialStep(
                "drop_zone",
                _("Great! Now you can drag and drop your mod ZIP files here.\n\nDon't have any mods yet? No worries! You can download them from ModAPI website.")
            ),
            TutorialStep(
                "mod_card",
                _("When you add mods, they'll appear as cards like this.\n\nYou can give them custom names (double-click to rename) and install them with one click!")
            ),
            TutorialStep(
                "language_button",
                _("Need the app in a different language?\nJust click this button to switch between available languages.")
            ),
            TutorialStep(
                "help_button",
                _("And that's it! If you ever need to see this tutorial again, just click the '?' button down here.\n\nHappy modding! 🎮")
            )
        ]

    def start(self):
        """Rozpoczyna tutorial"""
        self.current_step = 0
        self.overlay = TutorialOverlay(self.main_window)
        self._show_current_step()

    def next_step(self):
        """Przechodzi do następnego kroku"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._show_current_step()
        else:
            self.finish()

    def previous_step(self):
        """Wraca do poprzedniego kroku"""
        if self.current_step > 0:
            self.current_step -= 1
            self._show_current_step()

    def finish(self):
        """Kończy tutorial"""
        if self.overlay:
            self.overlay.destroy()
        if self.bubble:
            self.bubble.destroy()

        # Zapisz informację o ukończeniu tutoriala
        self.main_window.config.set_tutorial_shown(True)

    def _show_current_step(self):
        """Pokazuje aktualny krok"""
        step = self.steps[self.current_step]

        # Znajdź element do podświetlenia
        element = self.element_map.get(step.element_id)
        if not element:
            logger.error(f"Element not found: {step.element_id}")
            return

        # Podświetl element
        if self.overlay:
            self.overlay.highlight_element(element)

        # Usuń poprzedni dymek
        if self.bubble:
            self.bubble.destroy()

        # Pokaż nowy dymek
        self.bubble = TutorialBubble(
            self.main_window,
            step.message,
            element,
            on_next=self.next_step if not step.required_action else None,
            on_previous=self.previous_step if self.current_step > 0 else None,
            is_last=self.current_step == len(self.steps) - 1
        )
