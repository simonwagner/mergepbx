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

    return parser

def main():
    log = sys.stderr
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = args.mine

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
