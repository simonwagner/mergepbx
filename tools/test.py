#!/usr/bin/env python
import sys
import os
import logging
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

from . import helpers
from . import TEST_DIR

helpers.setup_path()

class OnlyTestLogsFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith("test.")

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s: %(message)s')

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return ch

if __name__ == '__main__':
    log_handler = None
    if "--logging" in sys.argv:
        setup_logging()
    if "--test-logging" in sys.argv and log_handler == None:
        handler = setup_logging()
        handler.addFilter(OnlyTestLogsFilter())

    loader = unittest.TestLoader()
    tests = loader.discover(TEST_DIR)
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
