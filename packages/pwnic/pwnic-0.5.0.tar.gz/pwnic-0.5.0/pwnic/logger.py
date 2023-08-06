import http
import logging
import logging.handlers

import colorlog
import requests
import urllib3
from rich.logging import RichHandler

from pwnic.config import config

log_level = getattr(logging, config.log_level)

# Create a logger
logger = logging.getLogger("pwnic")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.handlers.RotatingFileHandler(  # 1 MiB max
    filename="logs/test.log", maxBytes=1048576, backupCount=3
)
file_handler.setLevel(log_level)

# Create a console handler
console_handler = RichHandler(
    rich_tracebacks=True, tracebacks_suppress=[requests, urllib3, http]
)
console_handler.setLevel(logging.DEBUG)


# Create a formatter and add it to the handlers
log_colors: dict[str, str] = colorlog.default_log_colors
log_colors["CRITICAL"] = "white,bg_red"
file_formatter = colorlog.ColoredFormatter(
    fmt="%(asctime)s | %(name)s | %(log_color)s%(levelname)s%(reset)s | %(message)s",
    log_colors=log_colors,
)

file_handler.setFormatter(file_formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
