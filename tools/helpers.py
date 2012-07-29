import logging
import os
import sys

from . import SRC_DIR

def setup_path():
    sys.path.append(SRC_DIR)

def setup_logging(log_level = logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(levelname)s %(name)s - %(message)s')

    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
