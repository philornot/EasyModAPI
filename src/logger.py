"""
src/logger.py - Logging system with colors and formatting
"""
import logging
from datetime import datetime
from pathlib import Path

import coloredlogs

# Add custom WTF level
WTF = 60  # Higher than CRITICAL (50)
logging.addLevelName(WTF, 'WTF')


def wtf(self, message, *args, **kwargs):
    """
    What a Terrible Failure - for things that should NEVER happen.
    Log level borrowed from Android.
    """
    if self.isEnabledFor(WTF):
        self._log(WTF, message, args, **kwargs)


# Add wtf() method to Logger class
logging.Logger.wtf = wtf


class CustomFormatter(logging.Formatter):
    """
    Formatter generating logs in format:
    timestamp[tab]<file[tab]function: line>
    """

    def format(self, record):
        # Get timestamp in local timezone
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Extract filename from full path
        filename = Path(record.pathname).name

        # Format according to requirements
        location = f"<{filename}\t{record.funcName}: {record.lineno}>"

        # Combine everything with tabs
        prefix = f"{timestamp}\t{location}\t"

        # Add prefix to message
        return f"{prefix}{record.getMessage()}"


def cleanup_old_logs(log_dir: Path, max_logs: int = 15):
    """
    Remove oldest log files if their count exceeds max_logs.

    Args:
        log_dir (Path): Path to logs folder
        max_logs (int): Maximum number of log files to keep
    """
    # Find all .log files
    log_files = list(log_dir.glob("*.log"))

    # If there are more files than max_logs
    if len(log_files) > max_logs:
        # Sort by modification time (oldest first)
        log_files.sort(key=lambda x: x.stat().st_mtime)

        # Remove excess files (oldest ones)
        files_to_remove = len(log_files) - max_logs
        for i in range(files_to_remove):
            log_files[i].unlink()


def setup_logger(name="ForestModManager"):
    """
    Configure and return logger with colors and custom formatting.

    Args:
        name (str): Logger name

    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    logger.handlers = []

    # Prepare logs folder
    log_dir = Path.home() / '.forest_mod_manager' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Remove old logs if there are too many
    cleanup_old_logs(log_dir)

    # Create new log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"mod_manager_{timestamp}.log"

    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(CustomFormatter())
    logger.addHandler(fh)

    # Color configuration with WTF
    LEVEL_STYLES = {
        'debug': {'color': 'cyan'},
        'info': {'color': 'green'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True},
        'wtf': {'color': 'magenta', 'bold': True, 'background': 'black'}
    }

    # Console handler with colors
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt='%(asctime)s\t<%(filename)s\t%(funcName)s: %(lineno)d>\t%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level_styles=LEVEL_STYLES
    )

    return logger


# Usage example:
if __name__ == "__main__":
    logger = setup_logger()

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.wtf("How did this even happen?! 😱")

    # Show logs folder
    log_dir = Path.home() / '.forest_mod_manager' / 'logs'
    print("\nLogs folder:", log_dir)
    print("Current log files:")
    for log_file in sorted(log_dir.glob("*.log")):
        print(f"- {log_file.name}")
