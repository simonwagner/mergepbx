import sys
from argparse import ArgumentParser

from .nextstep import NSPlistReader

def get_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("file",
                        help="The file to parse")
    parser.add_argument("debug",
                        help="If an exception is thrown, start the debugger",
                        action="store_true")

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
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.debug:
        install_pdb_exception_handler()

    f = open(args.file)
    r = NSPlistReader(f, name=args.file)
    plist = r.read()

if __name__ == "__main__":
    main()
