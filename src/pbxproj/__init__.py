import codecs

from .pbxobjects import PBXProjFile
from . import core
from . import isa
from . import reader
from . import writer
from . import pbxobjects
from plist import NSPlistReader

def read(fname_or_f):
    #open file if fname_or_f is a string
    #else use it as f
    if isinstance(fname_or_f, str) or isinstance(fname_or_f, unicode):
        f = open(fname_or_f)
    else:
        f = fname_or_f
    #read project
    reader = NSPlistReader(f)
    return PBXProjFile(reader.read(), encoding=reader.get_encoding())

def write(fname_or_f, data, encoding=None):
    if encoding is None:
        encoding = data.get_encoding() or "utf-8"
    #open file if fname_or_f is a string
    #else use it as f
    if isinstance(fname_or_f, str) or isinstance(fname_or_f, unicode):
        f = codecs.open(fname_or_f, "w", encoding=encoding)
    else:
        f = fname_or_f
    #write project
    w = writer.PBXProjectPlistWriter(f)
    w.write_project(data)
