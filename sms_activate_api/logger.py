

import logging

logging_format = logging.Formatter(
    "%(levelname)s:[%(filename)s:%(lineno)s]:%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_format)

logger.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
