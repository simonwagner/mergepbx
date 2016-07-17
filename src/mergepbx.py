#!/usr/bin/env python

import sys
import os
import zipfile
from argparse import ArgumentParser
import io

from plist.nextstep import NSPlistReader
import pbxproj
from pbxproj.merge import merge_pbxs
from pbxproj.merge.pbxmerge import MergeException
import merge3

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("base",
                        help="base version - the last common version of mine and theirs")
    parser.add_argument("mine",
                        help="my version")
    parser.add_argument("theirs",
                        help="their version")
    parser.add_argument("-o", "--output",
                        help="output path for the merged file",
                        default=None)
    parser.add_argument("-d", "--debug",
                        help="enable debugger on exceptions",
                        action="store_true")
    parser.add_argument("--dump",
                        help="dump input files to the specified ZIP file(useful for debugging)",
                        default=None)
    parser.add_argument("--clean",
                        help="remove dangling file references in project files (obsolete, on by default)",
                        action="store_true",
                        default=True)
    parser.add_argument("--no-clean",
                        dest="clean",
                        help="don't remove dangling file references in project files",
                        action="store_false")

    return parser

def install_pdb_exception_handler():
    def info(type, value, tb):
       if hasattr(sys, 'ps1') or not sys.stderr.isatty():
          # we are in interactive mode or we don't have a tty-like
          # device, so we call the default hook
          sys.__excepthook__(type, value, tb)
       else:
          import traceback, pdb
          # we are NOT in interactive mode, print the exception...
          traceback.print_exception(type, value, tb)
          print
          # ...then start the debugger in post-mortem mode.
          pdb.pm()

    sys.excepthook = info

def main():
    log = sys.stderr
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = args.mine

    if args.dump is not None:
        #we have been asked to dump the files that will be merged
        dump_files(args.dump, args.base, args.mine, args.theirs)

    if args.debug:
        #if debugging is enabled, install the pdb
        #handler and let him handle the exception
        install_pdb_exception_handler()
        merge_pbx_files(args.base, args.mine, args.theirs, output, clean=args.clean)
    else:
        #if debugging is not enabled, simply report the exception
        try:
            merge_pbx_files(args.base, args.mine, args.theirs, output, clean=args.clean)
            sys.exit(0)
        except Exception as e:
            log.write("merging failed: %s\n" % str(e))
            log.write("falling back to 3-way text merge for Xcode project file...\n")


            merge_text_files(args.base, args.mine, args.theirs, output)
            sys.exit(1)

def merge_pbx_files(basef, minef, theirsf, mergedf, clean=False):
    base, mine, theirs = read_pbxs((basef, minef, theirsf))

    if clean:
        for name, project in zip((basef, minef, theirsf), (base, mine, theirs)):
            files_removed = project.clean_files()
            if len(files_removed) > 0:
                print "WARNING: %d dangling file references removed from %s" % (len(files_removed), name)


    merged_project = merge_pbxs(base, mine, theirs)

    pbxproj.write(mergedf, merged_project)

def read_pbxs(pbx_files):
    projects = [pbxproj.read(pbx_file) for pbx_file in pbx_files]

    return projects

def dump_files(dumpfile, base, mine, theirs):
    files = (base, mine, theirs)
    arcnames = ("base.pbxproj", "mine.pbxproj", "theirs.pbxproj")
    with zipfile.ZipFile(dumpfile, "w") as zf:
        for file, arcname in zip(files, arcnames):
            zf.write(file, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)

def merge_text_files(basef, minef, theirsf, mergedf):
    baselines, mylines, theirlines = [io.open(f, "r", encoding="utf-8").read().splitlines() for f in (basef, minef, theirsf)]
    result = merge3.merge(origtext=baselines, yourtext=mylines, theirtext=theirlines)
    mergedlines = result["body"]

    io.open(mergedf, "w", encoding="utf-8").write(str.join("\n", mergedlines))

if __name__ == "__main__":
    main()
