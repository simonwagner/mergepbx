#! /usr/bin/env python

import os
import sys
from collections import namedtuple
from git import Repo, GitCmdObjectDB

def main():
    repo_path, file_path, destination = sys.argv[1:4]

    collector = MergeCollector(repo_path)

    for hashes, file_contents in collector.itermerges(file_path):
        print "saving merge of %s and %s with %s as base" % (hashes.mine, hashes.theirs, hashes.base)
        dirname = str.join("-", hashes)
        full_dir_path = os.path.join(destination, dirname)

        os.mkdir(full_dir_path)

        for (name, file_content) in zip(("project.pbxproj.base", "project.pbxproj.mine", "project.pbxproj.theirs"), file_contents):
            full_file_path = os.path.join(full_dir_path, name)
            f = open(full_file_path, "w")
            f.write(file_content)
            f.close()

Merge = namedtuple("Merge", ("base", "mine", "theirs"))

class MergeCollector(object):
    def __init__(self, repo_path):
        repo = Repo(repo_path, odbt=GitCmdObjectDB)
        self.git = repo.git
        self.repo_path = repo_path

    def itermerges(self, filename):
        merges_with_base_iter = self._git_iter_merges_with_base_on_file(filename)

        for merge in merges_with_base_iter:
            base_content, mine_content, theirs_content = (self._git_show(commit, filename) for commit in merge)
            content_merge = Merge(base_content, mine_content, theirs_content)
            yield merge, content_merge

    def _git_iter_merges_with_base_on_file(self, filename):
        for (mine, theirs) in self._git_iter_merges_on_file(filename):
            base = self._git_get_merge_base(mine, theirs)

            yield Merge(base, mine, theirs)

    def _git_iter_merges_on_file(self, filename):
        log = self.git.log(filename)

        for line in log.splitlines():
            if line.startswith("Merge: "):
                line = line.replace("Merge: ", "", 1)
                parents = line.split()
                yield parents

    def _git_get_merge_base(self, a,b):
        return self.git.merge_base(a,b)[:7]

    def _git_show(self, commit, fname):
        file_repo_path = os.path.relpath(fname, self.repo_path)
        return self.git.show("%s:%s" % (commit, file_repo_path))

if __name__ == "__main__":
    main()
