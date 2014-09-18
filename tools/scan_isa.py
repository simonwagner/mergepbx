#!/usr/bin/env python

import logging
import sys
import os

from . import helpers
helpers.setup_path()

from plist.nextstep import NSPlistReader, NSPlistWriter
from pbxproj.isa import ISA_MAPPING

fname = sys.argv[1]
f = open(fname)
r = NSPlistReader(f, name=fname)
project = r.read()

objects = project["objects"]
isas = set(object["isa"] for object_id, object in objects.iteritems())

isas_known = set(ISA_MAPPING.iterkeys())

isas_unknown = isas - isas_known

if len(isas_unknown) == 0:
    print "no unknown objects"
else:
    for isa in sorted(isas_unknown):
        print isa
