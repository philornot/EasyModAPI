"""
src/ui/components.py - Reużywalne komponenty UI
"""
import zipfile
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from tkinterdnd2 import DND_FILES

from .styles import Colors, Styles
from ..logger import setup_logger

logger = setup_logger("Components")


class GradientButton(ctk.CTkButton):
    """Przycisk z gradientem i efektem hover"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(f"Created GradientButton with kwargs: {kwargs}")


class SecondaryButton(ctk.CTkButton):
    """Przycisk drugorzędny (outline)"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON_SECONDARY.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug(f"Created SecondaryButton with kwargs: {kwargs}")


class IconButton(ctk.CTkButton):
    """Przycisk z ikoną bez tła"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.ICON_BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)
        logger.debug("Created IconButton")


class Card(ctk.CTkFrame):
    """Karta z tłem i zaokrąglonymi rogami"""

    def __init__(self, *args, **kwargs):
        frame_kwargs = Styles.FRAME.copy()
        frame_kwargs.update(kwargs)
        super().__init__(*args, **frame_kwargs)
        logger.debug(f"Created Card with kwargs: {kwargs}")


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


class ModCard(Card):
    """Karta wyświetlająca informacje o przesłanym pliku ZIP"""

    def __init__(self, master, zip_path, on_install, on_remove, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.zip_path = Path(zip_path)

        # Frame na zawartość
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=8, pady=4)
        content.grid_columnconfigure(1, weight=1)

        # Nazwa pliku
        ctk.CTkLabel(
            content,
            text=self.zip_path.name,
            font=("Roboto", 13, "bold"),
            text_color=Colors.TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

        # Data dodania i liczba plików w jednym wierszu
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 4))

        # Data dodania
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        ctk.CTkLabel(
            info_frame,
            text=f"Dodano: {now}",
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left", padx=(0, 15))

        # Liczba modów
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                mod_count = len(zip_ref.namelist())
            mod_text = f"Liczba plików: {mod_count}"
        except:
            mod_text = "Nie można odczytać zawartości ZIP"

        ctk.CTkLabel(
            info_frame,
            text=mod_text,
            font=("Roboto", 11),
            text_color=Colors.TEXT_SECONDARY
        ).pack(side="left")

        # Przyciski
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        GradientButton(
            button_frame,
            text="Zainstaluj",
            width=90,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_install(self.zip_path)
        ).pack(side="left", padx=(0, 8))

        SecondaryButton(
            button_frame,
            text="Usuń",
            width=70,
            height=28,
            font=("Roboto", 12),
            command=lambda: on_remove(self)
        ).pack(side="left")


class FileDropZone(Card):
    """Strefa do przeciągania i upuszczania plików"""

    def __init__(self, master, on_file_drop, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_file_drop = on_file_drop
        logger.debug("Initializing FileDropZone")

        self.label = StatusLabel(
            self,
            text="Przeciągnij i upuść plik ZIP z modami\nlub kliknij aby wybrać",
            font=("Roboto", 14)
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=20)

        try:
            logger.debug("Registering DND handlers")
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._on_drop)
            self.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.dnd_bind('<<DragLeave>>', self._on_drag_leave)
        except Exception as e:
            logger.error(f"Failed to register DND handlers: {e}", exc_info=True)

        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)

        self._active = False
        self._drag_active = False

    def _on_drop(self, event):
        """Obsługa upuszczenia pliku"""
        if not self._active:
            logger.debug("Drop ignored - zone inactive")
            return

        try:
            file_path = event.data
            logger.info(f"File dropped: {file_path}")

            if str(file_path).lower().endswith('.zip'):
                self._drag_active = False
                self.configure(fg_color=Colors.CARD)
                self.on_file_drop(file_path)
            else:
                logger.warning(f"Invalid file type dropped: {file_path}")
                self.label.set_error("Tylko pliki ZIP!")
        except Exception as e:
            logger.error(f"Error handling file drop: {e}", exc_info=True)

    def _on_drag_enter(self, event):
        """Obsługa przeciągnięcia pliku nad strefę"""
        if self._active:
            logger.debug("Drag enter")
            self._drag_active = True
            self.configure(fg_color=Colors.SECONDARY)

    def _on_drag_leave(self, event):
        """Obsługa opuszczenia strefy przez przeciągany plik"""
        if self._active:
            logger.debug("Drag leave")
            self._drag_active = False
            self.configure(fg_color=Colors.CARD)

    def _on_click(self, event):
        """Obsługa kliknięcia"""
        if not self._active:
            logger.debug("Click ignored - zone inactive")
            return

        logger.debug("Opening file dialog")
        file_path = filedialog.askopenfilename(
            title="Wybierz plik ZIP z modami",
            filetypes=[("Pliki ZIP", "*.zip")]
        )

        if file_path:
            logger.info(f"File selected: {file_path}")
            self.on_file_drop(file_path)

    def activate(self):
        """Aktywuje strefę drop"""
        logger.info("Activating drop zone")
        self._active = True
        self.configure(fg_color=Colors.CARD)
        self.label.configure(
            text="Przeciągnij i upuść plik ZIP z modami\nlub kliknij aby wybrać",
            text_color=Colors.TEXT
        )

    def deactivate(self):
        """Dezaktywuje strefę drop"""
        logger.info("Deactivating drop zone")
        self._active = False
        self.configure(fg_color=Colors.CARD_HOVER)
        self.label.configure(
            text="Najpierw wybierz folder MODAPI!",
            text_color=Colors.WARNING
        )
