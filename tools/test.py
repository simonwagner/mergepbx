#!/usr/bin/env python
import sys
import os
import logging
from argparse import ArgumentParser
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

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("--logging",
                        help="show all log messages",
                        action="store_true")
    parser.add_argument("--test-logging",
                        help="show only log messages from test cases",
                        action="store_true")

    return parser

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

    parser = get_argument_parser()
    args = parser.parse_args()
    if args.logging:
        setup_logging()
    if args.test_logging and log_handler == None:
        handler = setup_logging()
        handler.addFilter(OnlyTestLogsFilter())

    loader = unittest.TestLoader()
    tests = loader.discover(TEST_DIR)
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
