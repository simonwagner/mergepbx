import re
from collections import OrderedDict
import codecs
from itertools import izip, izip_longest
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from .antlr import PlistLexer
from .antlr import PlistParser
from .antlr.runtime import antlr3

from .escape import escape_string

class NSParsingException(Exception):
    def __init__(self, line_nr, col_nr, name=None):
        self.name = name
        self.line_nr = line_nr
        self.col_nr = col_nr

        if self.name is None:
            message = "Parsing failure at line %r:%r" % (self.line_nr, self.col_nr)
        else:
            message = "Parsing failure at line %r:%r" % (self.line_nr, self.col_nr)

        super(NSParsingException, self).__init__(message)

class NSPlistReader(object):
    CODEC_DEF_RE = re.compile(r"^//\s*!\$\*(.+)\*\$!$") #e.g. "// !$*UTF8*$!"
    def __init__(self, f, name=None):
        self.f = f
        self.name = name

    def read(self):
        content = self.f.read()

        self._encoding = self._detect_encoding(content)
        unicode_content = unicode(content, encoding=self._encoding)
        stream = antlr3.ANTLRStringStream(unicode_content)
        lexer = PlistLexer(stream)
        tokens = antlr3.CommonTokenStream(lexer)
        parser = PlistParser(tokens)
        try:
            plist = parser.plist()
        except antlr3.exceptions.RecognitionException as e:
            raise NSParsingException(line_nr=e.line, col_nr=e.charPositionInLine, name=self.name)

        return plist

    def _detect_encoding(self, content):
        #first line may contain comment that
        #includes encoding of the file
        splitting = content.split("\n", 1)
        first_line = splitting[0]

        codec_def_match = self.__class__.CODEC_DEF_RE.match(first_line)
        if codec_def_match:
            codec_name = codec_def_match.group(1)
            return codec_name
        else:
            return "ascii"

    def get_encoding(self):
        return self._encoding

    def close(self):
        self.f.close()

class IndentWriter(object):
    ONLY_SPACES_RE = re.compile(r"\A\s+\Z")
    def __init__(self, f, indent_char="\t", indent_size=1):
        self.f = f
        self.indent_char = indent_char
        self.indent_size = indent_size
        self.indent_count = 0
        self.current_indent = ""

    def indent(self):
        self.indent_count += 1
        self.current_indent = self.indent_char*(self.indent_count*self.indent_size)

    def deindent(self):
        self.indent_count -= 1
        self.current_indent = self.indent_char*(self.indent_count*self.indent_size)

    def write(self, s):
        lines = s.splitlines(True)
        indendet_lines = (self.indent_line(line) for line in lines)
        self.f.write(str.join("", indendet_lines))

    def indent_line(self, line):
        if False:
            return line
        elif line.endswith("\n"):
            return line + self.current_indent
        else:
            return line

    def close(self):
        self.f.close()

class NSPlistWriter(IndentWriter):
    IDENTIFIER_RE = re.compile(r"^([A-Za-z0-9'_\.\$/]+)$")

    def __init__(self, f, codec="utf8"):
        super(NSPlistWriter, self).__init__(f, indent_char="\t", indent_size=1)
        self.codec = codec.upper()

    def write_plist(self, plist):
        self.write_header()
        self.write_value(plist)

    def write_header(self):
        self.write(u"// !$*%s*$!\n" % self.codec)

    def decide_multiline(self, value):
        return True

    def write_value(self, value):
        if isinstance(value, dict):
            multiline = self.decide_multiline(value)
            if multiline:
                self.write_dict_multiline(value)
            else:
                self.write_dict(value)
        elif isinstance(value, tuple) or isinstance(value, set) or isinstance(value, list):
            multiline = self.decide_multiline(value)
            if multiline:
                self.write_set_multiline(value)
            else:
                self.write_set(value)
        else:
            self.write_string(value)

    def write_string(self, string):
        if NSPlistWriter.IDENTIFIER_RE.match(string):
            self.write(string)
        else:
            self.write((u"\"%s\"" % escape_string(string)))

    def write_dict_multiline(self, dict, comments = {}):
        self.write(u"{")
        self.indent()

        for key, value in dict.iteritems():
            self.write(u"\n")
            if key in comments:
                comment = comments[key]
            else:
                comment = None

            self.write_dict_item(key, value, comment)

        self.deindent()
        self.write(u"\n}")

    def write_dict(self, dict, comments = {}):
        self.write(u"{")
        self.indent()

        for key, value in dict.iteritems():
            if key in comments:
                comment = comments[key]
            else:
                comment = None

            self.write_dict_item(key, value, comment)
            self.write(" ")

        self.deindent()
        self.write(u"}")

    def write_dict_item(self, key, value, comment = None):
        if isinstance(value, dict) or isinstance(value, tuple) or isinstance(value, set) or isinstance(value, list):
            comment_before_value = True
        else:
            comment_before_value = False

        self.write_dict_key(key, value, comment, comment_before_value)

        self.write(u" = ")
        self.write_value(value)
        self.write(u";")

        if not comment_before_value and comment != None:
            self.write(u" /*" + comment + u"*/ ")

    def write_dict_key(self, key, value, comment = None, comment_before_value = False):
        self.write_string(key)
        if comment_before_value and comment != None:
            self.write(u" /*" + comment + "*/ ")

    def write_set_multiline(self, values, comments = ()):
        self.write(u"(")
        self.indent()

        for value, comment in izip_longest(values, comments, fillvalue=None):
            self.write("\n")
            self.write_set_item(value, comment)
            self.write(u",")

        self.deindent()
        self.write(u"\n)")

    def write_set(self, values, comments = ()):
        self.write(u"(")

        for value, comment in izip_longest(values, comments, fillvalue=None):
            self.write_set_item(value, comment)
            self.write(u", ")

        self.write(u")")

    def write_set_item(self, value, comment = None):
        self.write_value(value)
        if comment != None:
            self.write(u" ")
            self.write_comment(comment)
