import re
import codecs

from plist import NSPlistWriter

class PBXProjectPlistWriter(NSPlistWriter):
    OBJECTID_RE = re.compile(r"^[0-9A-F]{24}")
    COMMENT_BLACKLIST = frozenset((
        "remoteGlobalIDString",
        "TargetAttributes",
    ))

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
        if key in self.COMMENT_BLACKLIST:
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

def write_pbx(fname_or_f, data, encoding=None):
    if encoding is None:
        encoding = data.get_encoding() or "utf-8"
    #open file if fname_or_f is a string
    #else use it as f
    if isinstance(fname_or_f, str) or isinstance(fname_or_f, unicode):
        f = codecs.open(fname_or_f, "w", encoding=encoding)
    else:
        f = fname_or_f
    #write project
    w = PBXProjectPlistWriter(f)
    w.write_project(data)
