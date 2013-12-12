import re
from collections import OrderedDict
from .antlr import PlistLexer
from .antlr import PlistParser
import antlr.runtime.antlr3 as antlr3


class NSPlistReader(object):
    def __init__(self, f):
        self.f = f

    def read(self):
        stream = antlr3.ANTLRInputStream(self.f)
        lexer = PlistLexer(stream)
        tokens = antlr3.CommonTokenStream(lexer)
        parser = PlistParser(tokens)
        plist = parser.plist()

        return plist

    def close(self):
        self.f.close()

class NSPlistWriter(object):
    def __init__(self, f, codec="UTF-8"):
        self.f = f
        self.codec = codec

    def write(self, data):
        self.f.write("// !$*%s*$!\n" % self.codec)
        self.walk_plist(self.f, data)

    def walk_plist(self, f, data):
        if hasattr(data, "iteritems"):
            self.walk_dictionary(f, data.iteritems())
        elif hasattr(data, "__iter__"):
            self.walk_array(f, data)
        else:
            raise Exception("unknown data type, must be either a dictionary or an array")

    def walk_dictionary(self, f, items):
        f.write("{")
        for key, value in items:
            key_bytes = key.encode(self.codec)
            f.write("\"%s\" = " % key_bytes.encode("string_escape"))
            self.walk_value(f, value)
            f.write("; ")
        f.write("}\n")

    def walk_array(self, f, items):
        f.write("(")
        for item in items:
            self.walk_value(f, item)
            f.write(", ")
        f.write(")\n")

    def walk_value(self, f, data):
        if hasattr(data, "iteritems"):
            self.walk_dictionary(f, data.iteritems())
        elif hasattr(data, "__iter__"):
            self.walk_array(f, data)
        else:
            f.write("\"%s\"" % str(data).encode("string_escape"))