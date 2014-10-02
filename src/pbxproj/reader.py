from plist import NSPlistReader
from .pbxobjects import PBXProjFile

def read_pbx(pbx_file, ignore_unknown_objects=False):
    fname_or_f = pbx_file
    #open file if fname_or_f is a string
    #else use it as f
    if isinstance(fname_or_f, str) or isinstance(fname_or_f, unicode):
        f = open(fname_or_f)
        fname = fname_or_f
    else:
        f = fname_or_f
        fname = None
    #read project
    reader = NSPlistReader(f, name=fname)
    return PBXProjFile(reader.read(), encoding=reader.get_encoding())
