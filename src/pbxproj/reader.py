from plist import NSPlistReader
from .pbxobjects import PBXProjFile

def read_pbx(pbx_file):
    f = open(pbx_file)
    r = NSPlistReader(f)
    plist = r.read()
    project = PBXProjFile(plist)
    r.close()

    return project