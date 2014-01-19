#!/usr/bin/env python
import sys
try:
    import cProfile as profile
except:
    import profile

from . import helpers
from . import TEST_DIR

helpers.setup_path()

import pbxproj
from pbxproj.merge import merge_pbxs

def main():
    if len(sys.argv) < 4:
        print "usage: %s base mine theirs [profile]" % sys.argv[0]
        return

    base, mine, theirs = sys.argv[1:-1]
    if len(sys.argv) >= 5:
        profile_out = sys.argv[-1]
    else:
        profile_out = None


    profile.runctx("merge_pbx_files(base, mine, theirs)", globals(), locals(), profile_out)

def merge_pbx_files(basef, minef, theirsf):
    base, mine, theirs = (pbxproj.read(f) for f in (basef, minef, theirsf))

    merged_project = merge_pbxs(base, mine, theirs)

if __name__ == "__main__":
    main()
