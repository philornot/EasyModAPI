from tkinter import filedialog

from tkdnd import DND_FILES

from .card import Card
from .labels import StatusLabel
from .ui.styles import Colors
from .. import _
from ..logger import setup_logger

logger = setup_logger()


class FileDropZone(Card):
    """Strefa do przeciągania i upuszczania plików"""

    def __init__(self, master, on_file_drop, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_file_drop = on_file_drop
        logger.debug(_("Initializing FileDropZone"))

        self.label = StatusLabel(
            self,
            text=_("Drop ZIP file with mods here\nor click to select"),
            font=("Roboto", 14)
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=20)

        try:
            logger.debug(_("Registering DND handlers"))
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._on_drop)
            self.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.dnd_bind('<<DragLeave>>', self._on_drag_leave)
        except Exception as e:
            logger.error(_("Failed to register DND handlers: {}").format(e), exc_info=True)

        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)

        self._active = False
        self._drag_active = False

    def _on_drop(self, event):
        """Obsługa upuszczenia pliku"""
        if not self._active:
            logger.debug(_("Drop ignored - zone inactive"))
            return

        try:
            file_path = event.data
            logger.info(_("File dropped: {}").format(file_path))

            if str(file_path).lower().endswith('.zip'):
                self._drag_active = False
                self.configure(fg_color=Colors.CARD)
                self.on_file_drop(file_path)
            else:
                logger.warning(_("Invalid file type dropped: {}").format(file_path))
                self.label.set_error(_("Tylko pliki ZIP!"))
        except Exception as e:
            logger.error(_("Error handling file drop: {}").format(e), exc_info=True)

    def _on_drag_enter(self, event):
        """Obsługa przeciągnięcia pliku nad strefę"""
        if self._active:
            logger.debug(_("Drag enter"))
            self._drag_active = True
            self.configure(fg_color=Colors.SECONDARY)

    def _on_drag_leave(self, event):
        """Obsługa opuszczenia strefy przez przeciągany plik"""
        if self._active:
            logger.debug(_("Drag leave"))
            self._drag_active = False
            self.configure(fg_color=Colors.CARD)

    def _on_click(self, event):
        """Obsługa kliknięcia"""
        if not self._active:
            logger.debug(_("Click ignored - zone inactive"))
            return

        logger.debug(_("Opening file dialog"))
        file_path = filedialog.askopenfilename(
            title=_("Wybierz plik ZIP z modami"),
            filetypes=[(_("Pliki ZIP"), "*.zip")]
        )

        if file_path:
            logger.info(_("File selected: {}").format(file_path))
            self.on_file_drop(file_path)

    def activate(self):
        """Aktywuje strefę drop"""
        logger.info(_("Activating drop zone"))
        self._active = True
        self.configure(fg_color=Colors.CARD)
        self.label.configure(
            text=_("Przeciągnij i upuść plik ZIP z modami\nlub kliknij aby wybrać"),
            text_color=Colors.TEXT
        )

    def deactivate(self):
        """Dezaktywuje strefę drop"""
        logger.info(_("Deactivating drop zone"))
        self._active = False
        self.configure(fg_color=Colors.CARD_HOVER)
        self.label.configure(
            text=_("Najpierw wybierz folder MODAPI!"),
            text_color=Colors.WARNING
        )
