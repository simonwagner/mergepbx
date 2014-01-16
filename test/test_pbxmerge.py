import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

import pbxproj.merge.pbxmerge as pbxmerge
import pbxproj.isa as isa

class PBXMergeTest(unittest.TestCase):
    def test_check_available_merger(self):
        isa_names = isa.ISA_MAPPING.keys()
        expected_mergers = set(isa_name + "Merger3" for isa_name in isa_names) - set(("PBXISAMerger3",))
        available_merger_names = set(pbxmerge.MERGER_MAPPING.keys())

        for expected_merger in expected_mergers:
            self.assertIn(expected_merger, available_merger_names, "Missing merger %s" % expected_merger)


if __name__ == '__main__':
    unittest.main()
