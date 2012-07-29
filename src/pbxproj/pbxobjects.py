from .core import DictionaryBoundObject
from . import isa

class PBXProjFile(DictionaryBoundObject):
    MAPPED_ATTRIBUTES = ("archiveVersion", "objectVersion", "rootObject")
    def __init__(self, plist):
        super(self.__class__, self).__init__(plist, self.__class__.MAPPED_ATTRIBUTES)
        self._plist = plist
        self._classes = PBXClasses(self._plist["classes"])
        self._objects = PBXObjects(self._plist["objects"])
        self._load_phases()

    def _load_phases(self):
        self._phases = dict()
        phases = (
            ("Frameworks", "PBXFrameworksBuildPhase"),
            ("Sources", "PBXSourcesBuildPhase"),
            ("Resources", "PBXResourcesBuildPhase")
        )

        for (section, phase_isa) in phases:
            phase_object = self._objects.getobject(phase_isa)
            if not phase_object is None:
                self._phases[section] = set(phase_object.files)

    def get_objects(self):
        return self._objects

    def phase_of_object(self, identifier):
        for phase, files in self._phases.iteritems():
            if identifier in files:
                return phase

class PBXClasses(object):
    def __init__(self, data_dict):
        self.data_dict = data_dict

class PBXObjects(object):
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def keys(self):
        return self.data_dict.keys()

    def get(self, key):
        return self._make_isa_object(key, self.data_dict[key])

    def iterobjects(self, isa=None):
        return (
            (key, self._make_isa_object(key, value)) for key, value in self.data_dict.iteritems() \
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
