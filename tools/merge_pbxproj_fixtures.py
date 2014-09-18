#!/usr/bin/env python

import logging
import sys
import os
from StringIO import StringIO
import os.path

from . import helpers
helpers.setup_path()

from plist.nextstep import NSPlistReader
import pbxproj
from pbxproj.pbxobjects import PBXProjFile
from pbxproj.merge import get_project_file_merger

def main():
    print sys.argv
    for directory in sys.argv[1:]:
        print "merging files in %s" % directory
        merge_fixtures(directory)

def read_pbxs(pbx_files):
    projects = []
    for pbx_file in pbx_files:
            f = open(pbx_file)
            r = NSPlistReader(f, name=pbx_file)
            plist = r.read()
            projects.append(PBXProjFile(plist))

    return projects

def merge_pbxs(base, mine, theirs):
    merger = get_project_file_merger()

    return merger.merge(base, mine, theirs)

def merge_pbx_files(basef, minef, theirsf, mergedf):
    base, mine, theirs = read_pbxs((basef, minef, theirsf))

    merged_project = merge_pbxs(base, mine, theirs)

    pbxproj.write(mergedf, merged_project)

def find_fixtures(path):
    dirlist = [os.path.join(path, entry) for entry in os.listdir(path)]
    directories = [entry for entry in dirlist if os.path.isdir(entry)]

    for directory in directories:
        merged_files = [os.path.join(directory, file) for file in ("project.pbxproj.base", "project.pbxproj.mine", "project.pbxproj.theirs")]
        files_exist = [os.path.exists(file) for file in merged_files]

        merged_files += [os.path.join(directory, "project.pbxproj.merged")]

        if reduce(lambda a, b: a and b, files_exist):
            yield tuple(merged_files)
        else:
            print "could not find files, skipping %s (%r)" % (directory, files_exist)
    return

def merge_fixtures(fixtures_dir):
    fixtures = find_fixtures(fixtures_dir)

    for fixture in fixtures:
        print \
            ("Merging \n" + \
            "\tbase: %s\n" + \
            "\tmine: %s\n" + \
            "\ttheirs: %s\n" + \
            "\tmerged: %s\n") % (fixture[0], fixture[1], fixture[2], fixture[3])
        merge_pbx_files(*fixture)

if __name__ == "__main__":
    main()
