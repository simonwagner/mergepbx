#!/usr/bin/env python

import sys
import os

from plist.nextstep import NSPlistReader
from pbxproj.writer import write_pbx
from pbxproj.reader import read_pbx
from pbxproj.merge import merge_pbxs
from pbxproj.merge.pbxmerge import MergeException

def main():
    log = sys.stderr
    if len(sys.argv) < 4:
        log.write("usage: mergepbx base mine theirs\n")
        sys.exit(os.EX_USAGE)

    base_path, mine_path, theirs_path = sys.argv[1:4]

    try:
        merge_pbx_files(base_path, mine_path, theirs_path, mine_path)
        sys.exit(0)
    except Exception as e:
        log.write("merging failed: %s\n" % str(e))
        sys.exit(1)

def merge_pbx_files(basef, minef, theirsf, mergedf):
    base, mine, theirs = read_pbxs((basef, minef, theirsf))

    merged_project = merge_pbxs(base, mine, theirs)

    mergedf = open(mergedf, "w")
    write_pbx(merged_project, mergedf)

def read_pbxs(pbx_files):
    projects = [read_pbx(pbx_file) for pbx_file in pbx_files]

    return projects

if __name__ == "__main__":
    main()