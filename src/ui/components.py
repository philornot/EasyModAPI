"""
src/ui/components.py - Reużywalne komponenty UI
"""
import customtkinter as ctk

from .styles import Colors, Styles


class GradientButton(ctk.CTkButton):
    """Przycisk z gradientem i efektem hover"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)


class SecondaryButton(ctk.CTkButton):
    """Przycisk drugorzędny (outline)"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.BUTTON_SECONDARY.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)


class IconButton(ctk.CTkButton):
    """Przycisk z ikoną bez tła"""

    def __init__(self, *args, **kwargs):
        button_kwargs = Styles.ICON_BUTTON.copy()
        button_kwargs.update(kwargs)
        super().__init__(*args, **button_kwargs)


class Card(ctk.CTkFrame):
    """Karta z tłem i zaokrąglonymi rogami"""

    def __init__(self, *args, **kwargs):
        frame_kwargs = Styles.FRAME.copy()
        frame_kwargs.update(kwargs)
        super().__init__(*args, **frame_kwargs)


class Title(ctk.CTkLabel):
    """Główny tytuł"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.TITLE.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)


class Subtitle(ctk.CTkLabel):
    """Podtytuł"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.SUBTITLE.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)


class StatusLabel(ctk.CTkLabel):
    """Label do wyświetlania statusu"""

    def __init__(self, *args, **kwargs):
        label_kwargs = Styles.LABEL.copy()
        label_kwargs.update(kwargs)
        super().__init__(*args, **label_kwargs)

    def set_success(self, text):
        """Ustawia tekst w stylu sukcesu"""
        self.configure(text=text, text_color=Colors.SUCCESS)

    def set_error(self, text):
        """Ustawia tekst w stylu błędu"""
        self.configure(text=text, text_color=Colors.ERROR)

    def set_warning(self, text):
        """Ustawia tekst w stylu ostrzeżenia"""
        self.configure(text=text, text_color=Colors.WARNING)
