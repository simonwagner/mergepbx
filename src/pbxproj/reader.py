try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from plist import NSPlistReader, XMLPlistReader
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
    #sniff the file and choose the right reader implementation
    reader_impl, f = _sniff_plist(f)
    #read project
    reader = reader_impl(f, name=fname)
    return PBXProjFile(reader.read(), encoding=reader.get_encoding())

def _sniff_plist(pbx_file):
    buffer = StringIO(pbx_file.read())
    pbx_file.close()
    first_line = buffer.readline()
    if "<?xml" in first_line:
        reader_impl = XMLPlistReader
    else:
        reader_impl = NSPlistReader

    #reset buffer
    buffer.reset()
    return (reader_impl, buffer)
