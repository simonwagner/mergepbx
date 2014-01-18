#!/usr/bin/env python

import logging
import sys
import os

from . import helpers
helpers.setup_path()

from plist.nextstep import NSPlistReader, NSPlistWriter

fname = sys.argv[1]
f = open(fname)
r = NSPlistReader(f)

w = NSPlistWriter(sys.stdout)
w.write(r.read())
