import sys
import logging
import os
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

import pbxproj
from testhelpers import fixture_path, make_logger, listpath, wrap_with_codec
from orderedset import OrderedSet
from collections import OrderedDict
import difflib

class PBXParsingTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PBXParsingTest, self).__init__(*args, **kwargs)
        self.logger = make_logger(self.__class__)

    def test_fixtures(self):
        parsing_fixtures_path = fixture_path("parse")

        project_files = [file for file in listpath(parsing_fixtures_path) if file.endswith(".pbxproj")]

        self.logger.debug("parsing %d files..." % len(project_files))

        for project_file in project_files:
            self.logger.debug("trying to parse file %s" % project_file)

            data = pbxproj.read(project_file)
            f_o = wrap_with_codec(StringIO(), data.get_encoding())
            pbxproj.write(f_o, data)

            #now compare the content of the written file with the original file
            #this should stay the same
            original_content = open(project_file).read()
            new_content = f_o.getvalue()
            f_o.close()

            #if assert will fail, generate a diff for this failure
            if not new_content == original_content:
                self.logger.error("failed to generate an exact replica, diff follows:")
                diff_lines = difflib.unified_diff(original_content.splitlines(), new_content.splitlines())
                for line in diff_lines:
                    self.logger.error(line)

            self.assertEquals(new_content, original_content, "%s was not correctly parsed" % project_file)
