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