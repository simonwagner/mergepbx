from itertools import izip, izip_longest
import re

def escape_string(s):
    escaped_s = s.encode("string_escape")
    #replace " with \", because string_escape does not do this
    escaped_s = escaped_s.replace("\"", "\\\"")
    #replace \' with ', because that is acceptable
    escaped_s = escaped_s.replace("\\'", "'")
    return escaped_s

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

class PlistWriter(IndentWriter):
    IDENTIFIER_RE = re.compile(r"^([^;\s=\(\)\{\}\,\"\<\>\+\-@]+)$")

    def __init__(self, f, codec="utf8"):
        super(PlistWriter, self).__init__(f, indent_char="\t", indent_size=1)
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
        if PlistWriter.IDENTIFIER_RE.match(string):
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
        self.write(u"(\n")
        self.indent()

        for value, comment in izip_longest(values, comments, fillvalue=None):
            self.write_set_item(value, comment)
            self.write(u",")

        self.deindent()
        self.write(u"\n)")

    def write_set_item(self, value, comment = None):
        self.write_value(value)
        if comment != None:
            self.write(u" ")
            self.write_comment(comment)

class PBXProjectPlistWriter(PlistWriter):
    OBJECTID_RE = re.compile(r"^[0-9A-F]{24}")

    def __init__(self, f):
        super(PBXProjectPlistWriter, self).__init__(f)
        self.multiline = True
        self.auto_comment = True

    def write_project(self, pbxproj):
        self.pbxproj = pbxproj
        self.write_header()
        self.write_project_dict(pbxproj)
        self.write("\n")

    def write_project_dict(self, pbxproj):
        plist = pbxproj._plist

        self.write("{")
        self.indent()

        for key, value in pbxproj._plist.iteritems():
            self.write("\n")
            if key == "objects":
                self.write_object_dict(pbxproj, value)
            elif key == "rootObject":
                self.write("rootObject = %s /* Project object */;" % pbxproj.rootObject)
            else:
                self.write_dict_item(key, value)

        self.deindent()
        self.write(u"\n}")

    def write_object_dict(self, pbxproj, object_dict):
        self.write("objects = {")
        self.indent()

        current_isa = None

        def compare_object_items(item1, item2):
            key1, value1 = item1
            key2, value2 = item2

            return cmp(value1["isa"], value2["isa"])

        sorted_object_items = sorted(object_dict.iteritems(), cmp=compare_object_items)

        for key, value in sorted_object_items:
            value_isa = value["isa"]
            if value_isa != current_isa:
                if current_isa != None:
                    self.deindent()
                    self.deindent()
                    self.write("\n/* End %s section */" % current_isa)
                    self.indent()
                    self.indent()

                self.deindent()
                self.deindent()
                self.write("\n\n/* Begin %s section */" % value_isa)
                self.indent()
                self.indent()

                current_isa = value_isa
            self.write("\n")
            if current_isa in set(("PBXFileReference", "PBXBuildFile")):
                self.multiline = False
            else:
                self.multiline = True

            self.write_dict_item(key, value)

        #write end of last section
        self.deindent()
        self.deindent()
        self.write("\n/* End %s section */" % current_isa)
        self.indent()
        self.indent()

        self.deindent()
        self.write(u"\n};")

    def decide_multiline(self, value):
        return self.multiline

    def write_dict_item(self, key, value, comment = None):
        if key == "remoteGlobalIDString":
            old = self.auto_comment
            self.auto_comment = False
            super(PBXProjectPlistWriter, self).write_dict_item(key, value, comment)
            self.auto_comment = old
        else:
            super(PBXProjectPlistWriter, self).write_dict_item(key, value, comment)

    def write_string(self, string):
        if self.auto_comment and PBXProjectPlistWriter.OBJECTID_RE.match(string):
            comment = self.get_comment_for_object(string)
            super(PBXProjectPlistWriter, self).write_string(string)
            if comment != None:
                self.write(" /* %s */" % comment)
        else:
            super(PBXProjectPlistWriter, self).write_string(string)

    def write_dict_key(self, key, value, comment = None, comment_before_value = False):
        if not isinstance(value, dict) or value.get("isa", None) != "PBXProject":
            super(PBXProjectPlistWriter, self).write_dict_key(key, value, comment, comment_before_value)
        else:
            comment = "Project object"
            super(PBXProjectPlistWriter, self).write_string(key)
            if comment_before_value and comment != None:
                self.write(u" /* " + comment + " */")

    def get_comment_for_object(self, identifier):
        try:
            object = self.pbxproj.get_objects().get(identifier)
        except KeyError:
            return None # if object does not exist, make no comment about it
        if object == None:
            return None
        else:
            return object.get_name(self.pbxproj)

def write_pbx(project, output):
    w = PBXProjectPlistWriter(output)
    w.write_project(project)