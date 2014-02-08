import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest
import os
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import difflib
from itertools import chain

import pbxproj
import pbxproj.merge.pbxmerge as pbxmerge
from pbxproj.merge import merge_pbxs
import pbxproj.isa as isa

from testhelpers import fixture_path, make_logger, listpath, wrap_with_codec

def first(iterable, predicate, default=None):
    for item in iterable:
        if predicate(item):
            return item
    return default

def load_merge_task(files_to_be_merged):
    postfixes = (".base", ".mine", ".theirs", ".merged")

    base, mine, theirs, merged = (first(
                                    files_to_be_merged,
                                    lambda file: file.endswith(postfix),
                                    None)
                                  for postfix
                                  in postfixes)
    return (base, mine, theirs, merged)

class PBXMergeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PBXMergeTest, self).__init__(*args, **kwargs)
        self.logger = make_logger(self.__class__)

    def test_check_available_merger(self):
        isa_names = isa.ISA_MAPPING.keys()
        expected_mergers = set(isa_name + "Merger3" for isa_name in isa_names) - set(("PBXISAMerger3",))
        available_merger_names = set(pbxmerge.MERGER_MAPPING.keys())

        for expected_merger in expected_mergers:
            self.assertIn(expected_merger, available_merger_names, "Missing merger %s" % expected_merger)

    def test_merge_fixtures(self):
        merge_fixtures_path = fixture_path("merge")
        merge_projects = listpath(merge_fixtures_path)
        merge_tasks = [listpath(merge_project) for merge_project in merge_projects]

        for merge_task in chain.from_iterable(merge_tasks):
            task_files = listpath(merge_task)
            project_files = load_merge_task(task_files)

            self.logger.info("merging base %s with my %s and their %s and comparing with %s..." % project_files)

            projects = [pbxproj.read(project_file) for project_file in project_files]
            base, mine, theirs, merged = projects

            merged_buffer = StringIO()
            merged_buffer = wrap_with_codec(merged_buffer, codec=base.get_encoding())
            merged_project = merge_pbxs(base, mine, theirs)
            pbxproj.write(merged_buffer, merged_project)

            #now compare the content of the written file with the original file
            #this should stay the same
            expected_merged_content = open(project_files[-1]).read()
            merged_content = merged_buffer.getvalue()
            merged_buffer.close()

            #if assert will fail, generate a diff for this failure
            if not merged_content == expected_merged_content:
                self.logger.error("failed to generate an exact replica, diff follows:")
                diff_lines = difflib.unified_diff(expected_merged_content.splitlines(), merged_content.splitlines())
                for line in diff_lines:
                    self.logger.error(line)

            self.assertEquals(merged_content, expected_merged_content, "%s was not correctly merged" % merge_task)

if __name__ == '__main__':
    unittest.main()
