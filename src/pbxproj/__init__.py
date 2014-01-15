from .pbxobjects import PBXProjFile
from . import core
from . import isa
from . import reader
from . import writer
from . import pbxobjects
from plist import NSPlistReader

def read(fname):
    f = open(fname)
    reader = NSPlistReader(f)
    return PBXProjFile(reader.read())

def write(fname_or_f, data, encoding="utf-8"):
    if isinstance(fname_or_f, str) or isinstance(fname_or_f, unicode):
        f = open(fname, "w", encoding=encoding)
    else:
        f = fname_or_f
    writer.write_pbx(data, f)
