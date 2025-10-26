# logger.py
#
# @author: Adrian Esteban Velasquez Solano
# @date: 10-2025
#
# In collaboration with CASA - Centro de Aseguramiento del Aprendizaje
# Universidad de los Andes
# Facultad de Administración
# Bogotá D.C., Colombia
#
# Description: This script provides logging functionality for the application. It defines a Logger class
# that can be used to log messages with different severity levels (INFO, WARNING, ERROR) to both the console and a log file.

# ================================================ IMPORTS ============================================================

import logging
import os
from datetime import datetime

# ================================================ CONSTANTS ==========================================================

LOGS_FOLDER = '../logs'
LOG_FILE = f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
COUNTER = 0


# =============================================== FORMATTER CLASS =====================================================

class ColoredFormatter(logging.Formatter):
    """
    Formatter that adds ANSI color codes to log messages for the console.
    INFO -> green, WARNING -> orange (ANSI 256-color 214), ERROR -> red.
    """
    COLORS = {
        logging.INFO: '\033[32m',  # green
        logging.WARNING: '\033[38;5;214m',  # orange (256-color)
        logging.ERROR: '\033[31m',  # red
    }
    RESET = '\033[0m'

    def format(self, record):
        """
        Format the log record with color codes.
        :param record: The log record to format.
        :return: The formatted log message with color codes.
        """
        formatted = super().format(record)
        color = self.COLORS.get(record.levelno, '')
        return f"{color}{formatted}{self.RESET}" if color else formatted


# ================================================ LOGGER CLASS ======================================================

# python
class Logger:
    """
    Logger class to handle logging messages to both console and a log file.
    Updated to use colored console output.
    """

    def __init__(self):
        fmt = '%(asctime)s - %(levelname)s - %(message)s'

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicate logs
        if root.handlers:
            for h in list(root.handlers):
                root.removeHandler(h)

        # Stream handler (colored)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(ColoredFormatter(fmt))

        root.addHandler(stream_handler)

        self._root = root
        self._fmt = fmt
        self._file_handler = None

    def _ensure_file_handler(self):
        """
        Create logs folder and file handler if not already created.
        Called lazily when an error is logged.
        """
        if self._file_handler is not None:
            return

        os.makedirs(LOGS_FOLDER, exist_ok=True)
        log_file = f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        log_path = os.path.join(LOGS_FOLDER, log_file)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self._fmt))

        self._root.addHandler(file_handler)
        self._file_handler = file_handler

    def info(self, message: str):
        """
        Log an info message.
        :param message: The info message to log.
        :return: None
        """
        logging.info(message)

    def warning(self, message: str):
        """
        Log a warning message.
        :param message: The warning message to log.
        :return: None
        """
        logging.warning(message)

    def error(self, message: str):
        """
        Log an error message.
        :param message: The error message to log.
        :return: None
        """
        try:
            self._ensure_file_handler()
        except Exception as e:
            # If file handler creation fails, still log the error to console
            logging.error(f"Failed to create log file: {e}")
        logging.error(message)

    def delete_logs(self):
        """
        Delete all log files in the logs folder.
        :return: None
        """
        count = 0
        if not os.path.exists(LOGS_FOLDER):
            self.info(f'No logs folder to delete files from: {LOGS_FOLDER}')
            return

        for filename in os.listdir(LOGS_FOLDER):
            file_path = os.path.join(LOGS_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
            except Exception as e:
                self.error(f'Error deleting log file {file_path}: {e}')
        self.info(f'Deleted {count} log files.')
