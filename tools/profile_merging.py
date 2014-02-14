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
from pbxproj.merge import merge_pbxs

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("base",
                        help="base for merging")
    parser.add_argument("mine",
                        help="mine for merging")
    parser.add_argument("theirs",
                        help="theirs for merging")
    parser.add_argument("-p", "--profile",
                        help="store profile under this file path",
                        default=None)
    parser.add_argument("-r", "--runs",
                        type=int,
                        help="how often should we parse the file",
                        default=1)

    return parser

def main():
    parser = get_argument_parser()
    args = parser.parse_args()


    profile.runctx("for i in range(args.runs): merge_pbx_files(args.base, args.mine, args.theirs)", globals(), locals(), args.profile)

def merge_pbx_files(basef, minef, theirsf):
    base, mine, theirs = (pbxproj.read(f) for f in (basef, minef, theirsf))

    merged_project = merge_pbxs(base, mine, theirs)

if __name__ == "__main__":
    main()
