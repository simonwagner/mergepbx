from plist import NSPlistReader
from .pbxobjects import PBXProjFile

def read_pbx(pbx_file, ignore_unknown_objects=False):
    f = open(pbx_file)
    r = NSPlistReader(f)
    plist = r.read()
    project = PBXProjFile(plist, ignore_unknown_objects=False)
    r.close()

    return project
