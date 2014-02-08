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
    parser.add_argument("--debug",
                        help="start the debugger when an exception is thrown",
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

def install_pdb_exception_handler():
    def info(type, value, tb):
       if hasattr(sys, 'ps1') or not sys.stderr.isatty():
          # we are in interactive mode or we don't have a tty-like
          # device, so we call the default hook
          sys.__excepthook__(type, value, tb)
       else:
          import traceback, pdb
          # we are NOT in interactive mode, print the exception...
          traceback.print_exception(type, value, tb)
          print
          # ...then start the debugger in post-mortem mode.
          pdb.pm()

    sys.excepthook = info

if __name__ == '__main__':
    log_handler = None

    parser = get_argument_parser()
    args = parser.parse_args()
    if args.logging:
        setup_logging()
    if args.test_logging and log_handler == None:
        handler = setup_logging()
        handler.addFilter(OnlyTestLogsFilter())
    if args.debug:
        install_pdb_exception_handler()

    loader = unittest.TestLoader()
    tests = loader.discover(TEST_DIR)

    if args.debug:
        print "Running tests in debug mode..."
        for test in tests:
            test.debug()
    else:
        testRunner = unittest.runner.TextTestRunner()
        testRunner.run(tests)
