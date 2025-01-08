from tkinter import filedialog

from tkdnd import DND_FILES

from src.i18n import _
from src.logger import setup_logger
from .card import Card
from .labels import StatusLabel
from .ui.styles import Colors

logger = setup_logger()


class FileDropZone(Card):
    """File drag and drop zone"""

    def __init__(self, master, on_file_drop, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_file_drop = on_file_drop
        logger.debug("Initializing FileDropZone")

        self.label = StatusLabel(
            self,
            text=_("Drop ZIP file with mods here\nor click to select"),
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
        """Handle file drop"""
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
                self.label.set_error(_("ZIP files only!"))
        except Exception as e:
            logger.error(f"Error handling file drop: {e}", exc_info=True)

    def _on_drag_enter(self, event):
        """Handle file drag enter"""
        if self._active:
            logger.debug("Drag enter")
            self._drag_active = True
            self.configure(fg_color=Colors.SECONDARY)

    def _on_drag_leave(self, event):
        """Handle file drag leave"""
        if self._active:
            logger.debug("Drag leave")
            self._drag_active = False
            self.configure(fg_color=Colors.CARD)

    def _on_click(self, event):
        """Handle click"""
        if not self._active:
            logger.debug("Click ignored - zone inactive")
            return

        logger.debug("Opening file dialog")
        file_path = filedialog.askopenfilename(
            title=_("Select ZIP file with mods"),
            filetypes=[(_("ZIP Files"), "*.zip")]
        )

        if file_path:
            logger.info(f"File selected: {file_path}")
            self.on_file_drop(file_path)

    def activate(self):
        """Activate drop zone"""
        logger.info("Activating drop zone")
        self._active = True
        self.configure(fg_color=Colors.CARD)
        self.label.configure(
            text=_("Drop ZIP file with mods here\nor click to select"),
            text_color=Colors.TEXT
        )

    def deactivate(self):
        """Deactivate drop zone"""
        logger.info("Deactivating drop zone")
        self._active = False
        self.configure(fg_color=Colors.CARD_HOVER)
        self.label.configure(
            text=_("Select MODAPI folder first!"),
            text_color=Colors.WARNING
        )
