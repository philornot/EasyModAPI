"""
src/ui/components/easter_egg.py - System easter egga z jeleniem
"""
import random

import customtkinter as ctk
from PIL import Image

from src import _
from src.components.ui.styles import Colors
from src.logger import setup_logger
from src.utils import get_asset_path

logger = setup_logger("EasterEgg")


class AnimatedDeer(ctk.CTkFrame):
    def __init__(self, master):
        logger.debug(_("Initializing AnimatedDeer"))
        super().__init__(
            master,
            fg_color="transparent",
            width=40,
            height=40
        )
        self._is_expanded = False
        self._animation_running = False

        # Załaduj obrazki
        logger.debug(_("Loading deer images"))
        try:
            self.small_image = ctk.CTkImage(
                light_image=Image.open(get_asset_path("assets/icons/deer1.png")),
                dark_image=Image.open(get_asset_path("assets/icons/deer1.png")),
                size=(40, 40)
            )

            self.full_image = ctk.CTkImage(
                light_image=Image.open(get_asset_path("assets/icons/deer2.png")),
                dark_image=Image.open(get_asset_path("assets/icons/deer2.png")),
                size=(200, 200)
            )
            logger.debug(_("Deer images loaded successfully"))
        except Exception as e:
            logger.error(_("Failed to load deer images: {}").format(e))
            raise

        # Label na obrazek
        self.image_label = ctk.CTkLabel(
            self,
            text="",
            image=self.small_image,
            cursor="hand2"
        )
        self.image_label.pack(expand=True, fill="both")

        # Bindy
        self.bind("<Button-1>", self._toggle_animation)
        self.image_label.bind("<Button-1>", self._toggle_animation)

        # Pozycjonowanie
        self.place(relx=0, rely=1.0, x=20, y=-20, anchor="sw")
        logger.debug(_("AnimatedDeer initialized and placed"))

        # Referencja do tekstu
        self.lyrics_label = None

    # noinspection PyUnusedLocal
    def _toggle_animation(self, event=None):
        """Przełącza stan animacji"""
        if self._animation_running:
            logger.debug(_("Animation already in progress, ignoring toggle"))
            return

        self._animation_running = True
        logger.debug(
            _("Toggling animation, current state: {}").format('expanded' if self._is_expanded else 'collapsed'))

        if self._is_expanded:
            self._restore_original_ui()
        else:
            # Create white overlay that covers everything
            logger.debug(_("Creating white overlay"))
            self.overlay = ctk.CTkFrame(self.master, fg_color=Colors.EASTER_EGG_OVERLAY)
            self.overlay.place(x=0, y=0, relwidth=1, relheight=1)

            # Skonfiguruj duży obrazek jelenia
            logger.debug(_("Configuring large deer image"))
            self.configure(width=200, height=200)
            self.image_label.configure(image=self.full_image)
            self.lift()  # Bring deer to front

            self._show_lyrics()

        self._is_expanded = not self._is_expanded
        self._animation_running = False
        logger.debug(_("Animation completed, new state: {}").format('expanded' if self._is_expanded else 'collapsed'))

    def _restore_original_ui(self):
        """Przywraca oryginalne UI"""
        logger.debug(_("Restoring original UI"))

        if hasattr(self, 'overlay'):
            logger.debug(_("Removing overlay"))
            self.overlay.destroy()

        if hasattr(self, 'lyrics_label'):
            logger.debug(_("Removing lyrics"))
            self.lyrics_label.destroy()

        # Przywróć mały rozmiar jelenia
        logger.debug(_("Restoring small deer"))
        self.configure(width=40, height=40)
        self.image_label.configure(image=self.small_image)
        self.place(relx=0, rely=1.0, x=20, y=-20, anchor="sw")

        # Odśwież widgety głównego okna
        self.master.update()
        logger.debug(_("Original UI restored"))

    def _show_lyrics(self):
        """Pokazuje tekst piosenki"""
        logger.debug(_("Showing lyrics"))
        if not self.lyrics_label:
            self.lyrics_label = ctk.CTkLabel(
                self.master,
                text="Bury your head\nhow can you sleep\nwhile the man that you loved\nburns at the stake",
                font=("Indie Flower", 32),
                text_color=Colors.EASTER_EGG_TEXT,
                fg_color=Colors.EASTER_EGG_OVERLAY,
                bg_color=Colors.EASTER_EGG_OVERLAY
            )
            self.lyrics_label.place(relx=0.5, rely=0.5, anchor="center")
            self.lyrics_label.lift()
            logger.debug(_("Lyrics displayed"))

    @staticmethod
    def should_appear(config) -> bool:
        chance = config.get_egg_chance()  # Remove any arguments
        should_appear = random.random() < chance
        logger.debug(_("Checking if deer should appear (chance {}%): {}").format(chance * 100, should_appear))
        return should_appear
