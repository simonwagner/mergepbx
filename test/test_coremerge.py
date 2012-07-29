import sys
import logging
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

from pbxproj.merge.coremerge import *
from orderedset import OrderedSet
from collections import OrderedDict

class CoreMergeTest(unittest.TestCase):
    def test_diff_dict_keys(self):
        base = {
            "a" : "base",
            "b" : "base",
            "c" : "base"
        }

        mine = {
            "a" : "base",
            "c" : "mine_conflict",
            "d" : "mine_new"
        }

        expected_added = set(("d",))
        expected_deleted = set(("b",))
        expected_common = set(("a", "c"))

        diff = diff_dict_keys(base, mine)

        self.assertEquals(expected_added, diff.added)
        self.assertEquals(expected_deleted, diff.deleted)
        self.assertEquals(expected_common, diff.common)

    def test_diff3_dict_keys(self):
        base = {
            "a" : "base",
            "b" : "base",
            "c" : "base",
            "e" : "base",
            "g" : "base",
        }

        mine = {
            "a" : "base",
            "c" : "mine_conflict",
            "d" : "mine_new",
            "e" : "base",
            "g" : "mine_conflict",
        }

        theirs = {
           "a" : "base",
           "c" : "theirs_conflict",
           "f" : "theirs_new",
        }

        expected_mine_added = set(("d",))
        expected_theirs_added = set(("f",))
        expected_deleted = set(("b",))
        expected_conflicting_deleted = set(("g", "e"))
        expected_common = set(("a", "c"))

        diff = diff3_dict_keys(base, mine, theirs)

        self.assertEquals(expected_mine_added, diff.mine_added)
        self.assertEquals(expected_theirs_added, diff.theirs_added)
        self.assertEquals(expected_conflicting_deleted, diff.conflicting_deleted)
        self.assertEquals(expected_deleted, diff.deleted)
        self.assertEquals(expected_common, diff.common)

    def test_diff_dict(self):
        base = {
            "a" : "base",
            "b" : "base",
            "c" : "base"
        }

        mine = {
            "a" : "base",
            "c" : "mine_updated",
            "d" : "mine_new"
        }

        expected_added = set(("d",))
        expected_updated = set(("c",))
        expected_deleted = set(("b",))
        expected_common = set(("a",))

        diff = diff_dict(base, mine)

        self.assertEquals(expected_added, diff.added)
        self.assertEquals(expected_updated, diff.updated)
        self.assertEquals(expected_deleted, diff.deleted)
        self.assertEquals(expected_common, diff.common)

    def test_diff3_dict(self):
        base = {
            "a" : "base",
            "b" : "base",
            "c" : "base",
            "e" : "base",
            "g" : "base",
            "h" : "base"
        }

        mine = {
            "a" : "base",
            "c" : "mine_conflict",
            "d" : "mine_new",
            "e" : "base",
            "g" : "mine_conflict",
            "h" : "mine"
        }

        theirs = {
           "a" : "base",
           "c" : "theirs_conflict",
           "f" : "theirs_new",
           "h" : "base"
        }

        expected_mine_added = set(("d",))
        expected_theirs_added = set(("f",))
        expected_mine_updated = set(("h",))
        expected_theirs_updated = set()
        expected_deleted = set(("b","e"))
        expected_conflicting = set(("c","g"))
        expected_common = set(("a",))

        diff = diff3_dict(base, mine, theirs)

        self.assertEquals(expected_mine_added, diff.mine_added)
        self.assertEquals(expected_mine_updated, diff.mine_updated)
        self.assertEquals(expected_theirs_added, diff.theirs_added)
        self.assertEquals(expected_theirs_updated, diff.theirs_updated)
        self.assertEquals(expected_conflicting, diff.conflicting)
        self.assertEquals(expected_deleted, diff.deleted)
        self.assertEquals(expected_common, diff.common)

    def test_diff_set(self):
        base = set((
            "a", "b", "c"
        ))
        mine = set((
            "a", "e", "d"
        ))
        theirs = set((
            "a", "f", "b", "c"
        ))

        expected_added = set((
            "e", "d", "f"
        ))
        expected_deleted = set((
            "b", "c"
        ))
        expected_common = set((
            "a"
        ))

        diff = diff3_set(base, mine, theirs)
        self.assertEquals(expected_added, diff.added)
        self.assertEquals(expected_deleted, diff.deleted)
        self.assertEquals(expected_common, diff.common)

    def test_merge_set(self):
        logger = logging.getLogger("test.CoreMergeTest.test_merge_set")

        base = set((
            "a", "b", "c"
        ))
        mine = set((
            "a", "e", "d"
        ))
        theirs = set((
            "a", "f", "b", "c"
        ))

        expected_merged = set((
            "a", "e", "d", "f"
        ))

        diff = diff3_set(base, mine, theirs)
        merged = merge_set(diff, base, mine, theirs)
        self.assertEquals(expected_merged, merged)

    def test_merge_ordered_set(self):
        logger = logging.getLogger("test.CoreMergeTest.test_merge_ordered_set")

        base = OrderedSet((
            "a", "b", "c"
        ))
        mine = OrderedSet((
            "a", "e", "d"
        ))
        theirs = OrderedSet((
            "a", "f", "b", "c"
        ))

        expected_merged = OrderedSet((
            "a", "e", "d", "f"
        ))

        diff = diff3_set(base, mine, theirs)
        merged = merge_ordered_set(diff, base, mine, theirs)

        self.assertEquals(tuple(expected_merged), tuple(merged))

        #test if we can apply it cleanly to theirs
        diff_theirs = diff3_set(theirs, theirs, merged)
        merged_theirs = merge_ordered_set(diff, theirs, theirs, merged)

        self.assertEquals(tuple(merged), tuple(merged_theirs))

    def test_merge_dict(self):
        base = {
            "a" : "base",
            "b" : "base",
            "c" : "base",
            "e" : "base",
            "g" : "base",
            "h" : "base"
        }

        mine = {
            "a" : "base",
            "c" : "base",
            "d" : "mine_new",
            "e" : "base",
            "g" : "base",
            "h" : "mine"
        }

        theirs = {
           "a" : "base",
           "c" : "theirs",
           "f" : "theirs_new",
           "h" : "base"
        }

        expected_merged = {
            "a" : "base",
            "c" : "theirs",
            "d" : "mine_new",
            "f" : "theirs_new",
            "h" : "mine"
        }

        diff = diff3_dict(base, mine, theirs)

        merged = merge_dict(diff, base, mine, theirs)

        self.assertEqual(merged, expected_merged)

    def test_merge_ordered_dict(self):
        base = OrderedDict((
            ("a", "base"),
            ("b", "base"),
            ("c", "base"),
            ("e", "base"),
            ("g", "base"),
            ("h", "base")
        ))

        mine = OrderedDict((
            ("a", "base"),
            ("c", "base"),
            ("d", "mine_new"),
            ("e", "base"),
            ("g", "base"),
            ("h", "mine")
        ))

        theirs = OrderedDict((
           ("a", "base"),
           ("c", "theirs"),
           ("f", "theirs_new"),
           ("h", "base"),
        ))

        expected_merged = OrderedDict((
            ("a", "base"),
            ("c", "theirs"),
            ("d", "mine_new"),
            ("f", "theirs_new"),
            ("h", "mine")
        ))

        diff = diff3_dict(base, mine, theirs)

        merged = merge_ordered_dict(diff, base, mine, theirs)

        self.assertEqual(merged, expected_merged)

    def test_pbx_merge(self):
        mine = OrderedSet((
				"a",
                "b"
		))

        theirs = OrderedSet((
            "a",
        ))

        base = OrderedSet((
            "a",
        ))

        expected_merged = OrderedSet((
            "a",
            "b"
        ))

        diff = diff3_set(base, mine, theirs)

        merged = merge_ordered_set(diff, base, mine, theirs)

        self.assertEquals(tuple(expected_merged), tuple(merged))

        #test if we can apply it cleanly to theirs
        diff_theirs = diff3_set(theirs, theirs, merged)
        merged_theirs = merge_ordered_set(diff, theirs, theirs, merged)

        self.assertEquals(tuple(merged), tuple(merged_theirs))
