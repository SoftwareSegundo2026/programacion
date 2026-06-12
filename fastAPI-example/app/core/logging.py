import logging
from logging import Logger
from pathlib import Path


_CONFIGURED_LOGGERS: set[str] = set()


def setup_logging(log_file_path: str, level: str = "INFO") -> None:
    """Configura el sistema de logs: escribe en consola y en un archivo .log."""
    root_logger = logging.getLogger()

    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    root_logger.setLevel(numeric_level)

    has_file_handler = any(
        isinstance(handler, logging.FileHandler)
        and Path(getattr(handler, "baseFilename", "")) == log_path.resolve()
        for handler in root_logger.handlers
    )

    has_console_handler = any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers)

    if not has_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if not has_file_handler:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


def get_logger(name: str) -> Logger:
    """Devuelve un 'logger' para que cada módulo escriba sus propios mensajes de seguimiento."""
    if name in _CONFIGURED_LOGGERS:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    _CONFIGURED_LOGGERS.add(name)
    return logger