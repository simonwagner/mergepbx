from argparse import ArgumentParser
import csv
import os
from subprocess import check_output
from tempfile import mkdtemp
import shutil
import time
import sys
import gc
import numpy as np
import scipy
from scipy.stats import t
try:
    import cProfile as profile
except:
    print "WARNING: could not load cProfile, results may not be comparable!"
    import profile
import pstats

from . import reloader
from . import helpers
from . import PROJECT_DIR, TEST_DIR

#files that are used for the benchmark
BENCHMARK_FILES = (
    [os.path.join(TEST_DIR, file) for file in (
        "fixtures/merge/iosbsh/c95f65c-86c9e3b-fdcc4a7/project.pbxproj.base",
        "fixtures/merge/iosbsh/c95f65c-86c9e3b-fdcc4a7/project.pbxproj.mine",
        "fixtures/merge/iosbsh/c95f65c-86c9e3b-fdcc4a7/project.pbxproj.theirs"
    )],
)


def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("--start",
                        help="ref where to start",
                        default="HEAD")
    parser.add_argument("--stop",
                        help="ref where to stop",
                        default="origin/master")
    parser.add_argument("-o",
                        help="benchmark outputfile",
                        default="benchmark.csv")

    return parser


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    repo = Repo(PROJECT_DIR)
    tmp_repo = clone_repository(PROJECT_DIR)

    tmp_project = tmp_repo.working_dir
    tmp_src = os.path.join(tmp_project, "src")

    #add the temporary repository to the
    #load path. Add it to the beginning,
    #so we are sure that our modules
    #are loaded first
    sys.path = [tmp_src] + sys.path

    #enable reloader now
    reloader.enable(
        blacklist=lambda module: not module.__file__.startswith(tmp_src)
    )

    #import module to benchmark
    import pbxproj

    #now execute the benchmark for each commit
    for commit in walk_history(repo, args.start, args.stop):
        sys.stdout.write("Benchmarking %s" % commit)
        sys.stdout.flush()

        checkout_commit(tmp_repo, commit)
        clean_pyc(tmp_src)
        #first reload to get all new dependencies
        pbxproj = reload_pbxproj(repo, pbxproj)
        #then reload for real
        pbxproj = reload_pbxproj(repo, pbxproj)

        sys.stdout.write("...")
        sys.stdout.flush()
        result = run_benchmark(pbxproj, BENCHMARK_FILES, timer_impl=ClockTimer)
        sys.stdout.write(" [%gs, %gs]\n" % result.confidence_interval())

    reloader.disable()

    #delete temporary repo
    shutil.rmtree(tmp_repo.git_dir)
    shutil.rmtree(tmp_repo.working_dir)


class ProfileTimer(object):
    def __enter__(self):
        self._profile = profile.Profile()
        self._profile.enable()

    def __exit__(self, type, value, traceback):
        # Error handling here
        self._profile.disable()
        self._profile.create_stats()

    def duration_in_seconds(self):
        stats = pstats.Stats(self._profile)
        return stats.total_tt

class ClockTimer(object):
    def __enter__(self):
        self._start = time.time()

    def __exit__(self, type, value, traceback):
        # Error handling here
        self._finish = time.time()

    def duration_in_seconds(self):
        return self._finish - self._start


class BenchmarkResult(object):
    def __init__(self, results):
        self.results = results

    def avg(self):
        return sum(self.results)/len(self.results)

    def confidence_interval(self, confidence=0.95):
        a = 1.0*np.array(self.results)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t._ppf((1+confidence)/2., n-1)
        return m-h, m+h

class Repo(object):
    def __init__(self, working_dir, git_dir=None):
        if git_dir is None:
            git_dir = os.path.join(working_dir, ".git")

        self.working_dir = working_dir
        self.git_dir = git_dir

    def cmd(self, git_cmd, git_cmd_args):
        args = [
            "git",
            "--git-dir", self.git_dir,
            "--work-tree", self.working_dir,
            git_cmd
        ] + git_cmd_args

        return check_output(args)

def clone_repository(orig_repro):
    temp_repro = mkdtemp()

    args = ["git", "clone",
        "-s", "-q",
        orig_repro,
        temp_repro
    ]
    check_output(args)
    return Repo(temp_repro)


def walk_history(repo, start, stop):
    args = [
        "--format=format:%h",
        "--topo-order",
        "--reverse",
        "%s..%s" % (start, stop)
    ]
    log = repo.cmd("log", args)
    return (sha for sha in log.splitlines())


def checkout_commit(repo, commit):
    repo.cmd("checkout", ["-q", commit])


def clean_pyc(path):
    for root, dirs, files in os.walk('/home/paulo-freitas'):
        pyc_files = (file for file in files if file.endswith(".pyc"))
        for pyc_file in pyc_files:
            os.remove(os.path.join(root, pyc_file))


def reload_pbxproj(repo, pbxproj):
    reloader.reload(pbxproj)
    return pbxproj


def run_benchmark(pbxproj, test_files, runs=10, timer_impl=ProfileTimer):
    timer = timer_impl()

    results = [-1.0]*runs
    for i in range(runs):
        gc.collect()
        with timer:
            for test_file in test_files:
                basef, minef, theirsf = test_file

                base, mine, theirs = (pbxproj.read(f) for f in (basef, minef, theirsf))
                pbxproj.merge.merge_pbxs(base, mine, theirs)

        results[i] = timer.duration_in_seconds()

    return BenchmarkResult(results)

if __name__ == "__main__":
    main()
