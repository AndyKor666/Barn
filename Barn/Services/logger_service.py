import logging
import os

class LoggerService:
    _logger = None
    @staticmethod
    def get_logger():
        if LoggerService._logger:
            return LoggerService._logger

        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        barn_dir = os.path.join(documents_path, "Barn")
        os.makedirs(barn_dir, exist_ok=True)

        log_path = os.path.join(barn_dir, "Barn.log")

        logger = logging.getLogger("BarnLogger")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info("======== INFO SAVED ========")
        LoggerService._logger = logger
        return logger
