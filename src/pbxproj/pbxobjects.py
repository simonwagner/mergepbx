from itertools import chain

from .core import DictionaryBoundObject
from . import isa

class PBXProjFile(DictionaryBoundObject):
    MAPPED_ATTRIBUTES = ("archiveVersion", "objectVersion", "rootObject")
    def __init__(self, plist, ignore_unknown_objects=False, encoding=None):
        super(self.__class__, self).__init__(plist, self.__class__.MAPPED_ATTRIBUTES)
        self._plist = plist
        self._classes = PBXClasses(self._plist["classes"])
        self._objects = PBXObjects(self._plist["objects"], ignore_unknown_objects)
        self._load_phases()
        self._encoding = encoding

    def _load_phases(self):
        phases = []

        for identifier, object in self._objects.getobjects():
            if isinstance(object, isa.AbstractPBXBuildPhase):
                phases.append(object)

        self._phases_files = {
            phase : set(phase.files) for phase in phases
        }

    def get_objects(self):
        return self._objects

    def phase_of_object(self, identifier):
        for phase, files in self._phases_files.iteritems():
            if identifier in files:
                return phase.get_name(self)

    def get_encoding(self):
        return self._encoding

    def clean_files(self):
        #remove PBXBuildFile entries that are no longer referenced
        files = self._objects.getobjects(isa="PBXBuildFile")
        removed_files = []
        for (identifier, file) in files:
            if not file.has_attr("fileRef"):
                continue
            if not file.fileRef in self._objects:
                removed_files.append(identifier)
                self._objects.delete(identifier)

        return removed_files


class PBXClasses(object):
    def __init__(self, data_dict):
        self.data_dict = data_dict

class PBXObjects(object):
    def __init__(self, data_dict, ignore_unknown_objects):
        self.data_dict = data_dict
        self.ignore_unknown_objects = ignore_unknown_objects

    def keys(self):
        return self.data_dict.keys()

    def get(self, key, default=Ellipsis):
        if key not in self.data_dict and default is not Ellipsis:
            return default
        return self._make_isa_object(key, self.data_dict[key])

    def __contains__(self, key):
        return key in self.data_dict

    def delete(self, key):
        del self.data_dict[key]

    def iterobjects(self, isa=None):
        if self.ignore_unknown_objects:
            items_iter = ((key, value) for key,value in self.data_dict.iteritems() if isa.is_known(value["isa"]))
        else:
            items_iter = self.data_dict.iteritems()

        return (
            (key, self._make_isa_object(key, value)) for key, value in items_iter \
            if isa == None or value["isa"] == isa
        )

    def getobjects(self, isa=None):
        return tuple(self.iterobjects(isa))

    def getobject(self, isa):
        found_objects = self.getobjects(isa)

        if len(found_objects) >= 1:
            return self.getobjects(isa)[0][1]
        else:
            return None

    def _make_isa_object(self, identifier, isa_dict):
        return isa.create(identifier, isa_dict)
