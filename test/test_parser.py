import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest
import difflib

class ParserTest(unittest.TestCase):
    pass
