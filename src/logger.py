"""
src/logger.py - System logowania z kolorami i formatowaniem
"""
import logging
import coloredlogs
import os
from datetime import datetime
from pathlib import Path
import glob

# Dodaj własny poziom WTF
WTF = 60  # Wyższy niż CRITICAL (50)
logging.addLevelName(WTF, 'WTF')


def wtf(self, message, *args, **kwargs):
    """
    What a Terrible Failure - dla rzeczy, które NIGDY nie powinny się zdarzyć.
    Poziom logu zapożyczony z Androida.
    """
    if self.isEnabledFor(WTF):
        self._log(WTF, message, args, **kwargs)


# Dodaj metodę wtf() do klasy Logger
logging.Logger.wtf = wtf


class CustomFormatter(logging.Formatter):
    """
    Formatter generujący logi w formacie:
    timestamp[tab]<plik[tab]funkcja: linijka>
    """

    def format(self, record):
        # Pobierz timestamp w strefie lokalnej
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Wyciągnij nazwę pliku z pełnej ścieżki
        filename = Path(record.pathname).name

        # Sformatuj zgodnie z wymaganiami
        location = f"<{filename}\t{record.funcName}: {record.lineno}>"

        # Połącz wszystko z tabulatorami
        prefix = f"{timestamp}\t{location}\t"

        # Dodaj prefix do wiadomości
        return f"{prefix}{record.getMessage()}"


def cleanup_old_logs(log_dir: Path, max_logs: int = 15):
    """
    Usuwa najstarsze pliki logów, jeśli ich liczba przekracza max_logs.

    Args:
        log_dir (Path): Ścieżka do folderu z logami
        max_logs (int): Maksymalna liczba plików logów do zachowania
    """
    # Znajdź wszystkie pliki .log
    log_files = list(log_dir.glob("*.log"))

    # Jeśli jest więcej plików niż max_logs
    if len(log_files) > max_logs:
        # Sortuj po czasie modyfikacji (najstarsze pierwsze)
        log_files.sort(key=lambda x: x.stat().st_mtime)

        # Usuń nadmiarowe pliki (najstarsze)
        files_to_remove = len(log_files) - max_logs
        for i in range(files_to_remove):
            log_files[i].unlink()


def setup_logger(name="ForestModManager"):
    """
    Konfiguruje i zwraca logger z kolorami i customowym formatowaniem.

    Args:
        name (str): Nazwa loggera

    Returns:
        logging.Logger: Skonfigurowany logger
    """
    # Stwórz logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Wyczyść istniejące handlery
    logger.handlers = []

    # Przygotuj folder na logi
    log_dir = Path.home() / '.forest_mod_manager' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Usuń stare logi jeśli jest ich za dużo
    cleanup_old_logs(log_dir)

    # Stwórz nowy plik logu z timestampem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"mod_manager_{timestamp}.log"

    # Handler dla pliku
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(CustomFormatter())
    logger.addHandler(fh)

    # Konfiguracja kolorów z dodanym WTF
    LEVEL_STYLES = {
        'debug': {'color': 'cyan'},
        'info': {'color': 'green'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True},
        'wtf': {'color': 'magenta', 'bold': True, 'background': 'black'}
    }

    # Handler dla konsoli z kolorami
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt='%(asctime)s\t<%(filename)s\t%(funcName)s: %(lineno)d>\t%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level_styles=LEVEL_STYLES
    )

    # Zaloguj informację o nowym pliku
    logger.info(f"Started logging to: {log_file.name}")

    return logger


# Przykład użycia:
if __name__ == "__main__":
    logger = setup_logger()

    logger.debug("To jest debug message")
    logger.info("To jest info message")
    logger.warning("To jest warning message")
    logger.error("To jest error message")
    logger.critical("To jest critical message")
    logger.wtf("Co do... jak to się w ogóle stało?! 😱")

    # Pokaż folder z logami
    log_dir = Path.home() / '.forest_mod_manager' / 'logs'
    print("\nFolder z logami:", log_dir)
    print("Aktualne pliki logów:")
    for log_file in sorted(log_dir.glob("*.log")):
        print(f"- {log_file.name}")