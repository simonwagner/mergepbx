#!/usr/bin/env python
import sys
from argparse import ArgumentParser
try:
    import cProfile as profile
except:
    import profile

from . import helpers
from . import TEST_DIR

helpers.setup_path()

import pbxproj

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("file",
                        help="file to be parsed during the profiling")
    parser.add_argument("-p", "--profile",
                        help="store profile under this file path",
                        default=None)
    parser.add_argument("-r", "--runs",
                        type=int,
                        help="how often should we merge the file",
                        default=1)

    return parser

def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    profile.runctx("for i in range(runs): pbxproj.read(file)",
        globals={},
        locals=dict(
            pbxproj=pbxproj, file=args.file, runs=args.runs
        ),
        filename=args.profile)



if __name__ == "__main__":
    main()
