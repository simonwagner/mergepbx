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

def main():
    if len(sys.argv) < 2:
        print "usage: %s file [profile]" % sys.argv[0]
        return

    if len(sys.argv) >= 3:
        profile_out = sys.argv[2]
    else:
        profile_out = None


    profile.run("pbxproj.read(sys.argv[1])", profile_out)



if __name__ == "__main__":
    main()
