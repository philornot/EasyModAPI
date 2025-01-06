"""
src/__init__.py - Inicjalizacja głównego pakietu
"""
from .config import Config
from .installer import ModInstaller

__version__ = "1.0.0"

__all__ = [
    'Config',
    'ModInstaller'
]