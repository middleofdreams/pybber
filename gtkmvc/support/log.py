# this simple module offers a logger

import logging

# change this to set a different logging level
logger_level = logging.INFO

# gtkmvc uses this logger for its business
logger = logging.getLogger("gtkmvc")

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logger_level)
formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

