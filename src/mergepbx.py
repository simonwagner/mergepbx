#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser

from plist.nextstep import NSPlistReader
import pbxproj
from pbxproj.merge import merge_pbxs
from pbxproj.merge.pbxmerge import MergeException

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("base",
                        help="base version - the last common version of mine and theirs")
    parser.add_argument("mine",
                        help="my version")
    parser.add_argument("theirs",
                        help="their version")
    parser.add_argument("-o", "--output",
                        help="output path for the merged file",
                        default=None)
    parser.add_argument("-d", "--debug",
                        help="enable debugger on exceptions",
                        action="store_true")

    return parser

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

def main():
    log = sys.stderr
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = args.mine

    if args.debug:
        #if debugging is enabled, install the pdb
        #handler and let him handle the exception
        install_pdb_exception_handler()
        merge_pbx_files(args.base, args.mine, args.theirs, output)
    else:
        #if debugging is not enabled, simply report the exception
        try:
            merge_pbx_files(args.base, args.mine, args.theirs, output)
            sys.exit(0)
        except Exception as e:
            log.write("merging failed: %s\n" % str(e))
            sys.exit(1)

def merge_pbx_files(basef, minef, theirsf, mergedf):
    base, mine, theirs = read_pbxs((basef, minef, theirsf))

    merged_project = merge_pbxs(base, mine, theirs)

    mergedf = open(mergedf, "w")
    pbxproj.write(mergedf, merged_project)

def read_pbxs(pbx_files):
    projects = [pbxproj.read(pbx_file) for pbx_file in pbx_files]

    return projects

if __name__ == "__main__":
    main()
