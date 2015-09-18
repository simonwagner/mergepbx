from .core import DictionaryBoundObject
from inspect import isclass
import abc

class PBXISA(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, identifier, *args, **kwargs):
        self._identifier = identifier
        super(PBXISA, self).__init__(identifier, *args, **kwargs)

    @abc.abstractmethod
    def get_name(self, project):
        raise NotImplementedError

    def get_identifier(self):
        return self._identifier

class PBXISADictionaryBound(DictionaryBoundObject):
    def __init__(self, identifier, isa_dict, *args, **kwargs):
        super(PBXISADictionaryBound, self).__init__(isa_dict, *args, **kwargs)

class PBXBuildFile(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXBuildFile, self).__init__(*args, **kwargs)

    def get_name(self, project):
        if self.has_attr("fileRef"):
            fileRef = self.fileRef
            file = project.get_objects().get(fileRef)
            name = file.get_name(project)
        else:
            name = "(null)"
        container = project.phase_of_object(self._identifier)

        return "%s in %s" % (name, container)

class AbstractPBXBuildPhase(PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(AbstractPBXBuildPhase, self).__init__(*args, **kwargs)

    def get_name(self, project):
        if self.has_attr("name"):
            name = self.name
            return name
        else:
            default_name = getattr(self.__class__, "DEFAULT_NAME", None)
            if default_name is not None:
                return default_name
            else:
                return "(null)"

class PBXCopyFilesBuildPhase(AbstractPBXBuildPhase, PBXISA):
    pass

class PBXFrameworksBuildPhase(AbstractPBXBuildPhase, PBXISA):
    DEFAULT_NAME = "Frameworks"

class PBXResourcesBuildPhase(AbstractPBXBuildPhase, PBXISA):
    DEFAULT_NAME = "Resources"

class PBXShellScriptBuildPhase(AbstractPBXBuildPhase, PBXISA):
    DEFAULT_NAME = "ShellScript"

class PBXSourcesBuildPhase(AbstractPBXBuildPhase, PBXISA):
    DEFAULT_NAME = "Sources"

class PBXHeadersBuildPhase(AbstractPBXBuildPhase, PBXISA):
    DEFAULT_NAME = "Headers"

class PBXContainerItemProxy(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXContainerItemProxy, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return "PBXContainerItemProxy"

class PBXFileReference(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXFileReference, self).__init__(*args, **kwargs)

    def get_name(self, project):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.path.split("/")[-1]

class PBXGroup(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXGroup, self).__init__(*args, **kwargs)

    def get_name(self, project):
        if hasattr(self, "name"):
            return self.name
        elif hasattr(self, "path"):
            return self.path
        else:
            return None

class PBXLegacyTarget(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXLegacyTarget, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return self.name

class PBXNativeTarget(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXNativeTarget, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return self.name

class PBXProject(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXProject, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return "Project object"

    def get_project_name(self, project):
        targets = self.targets
        objects = project.get_objects()
        target_names = [objects.get(target).name for target in targets]

        return target_names[0]

class PBXReferenceProxy(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXReferenceProxy, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return self.path

class PBXTargetDependency(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXTargetDependency, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return "PBXTargetDependency"

class PBXVariantGroup(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(PBXVariantGroup, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return self.name

class XCBuildConfiguration(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(XCBuildConfiguration, self).__init__(*args, **kwargs)

    def get_name(self, project):
        return self.name

class XCConfigurationList(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(XCConfigurationList, self).__init__(*args, **kwargs)

    def get_name(self, project):
        targets = self.get_targets(project)
        target = targets[0]

        if isinstance(target, PBXProject):
            project_name = target.get_project_name(project)
            #whitespaces apparently get removed by XCode
            #so we need to remove them too.
            target_name = str.join("", project_name.split())
        else:
            target_name = target.get_name(project)

        return "Build configuration list for %s \"%s\"" % (target.isa, target_name)

    def get_targets(self, project):
        targets = []
        identifier = self.get_identifier()

        for object_identifier, object in project.get_objects().iterobjects():
            if hasattr(object, "buildConfigurationList"):
                if object.buildConfigurationList == identifier:
                    targets.append(object)
        return targets

class XCVersionGroup(PBXISA, PBXISADictionaryBound):
    def __init__(self, *args, **kwargs):
        super(XCVersionGroup, self).__init__(*args, **kwargs)

    def get_name(self, project):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.path

local_vars = dict(locals())
ISA_MAPPING = dict(
    ((clazz.__name__, clazz) for varname, clazz in local_vars.iteritems() if isclass(clazz) and issubclass(clazz, PBXISA))
)

def is_known(isa):
    return isa in ISA_MAPPING

def create(identifier, isa_dict):
    isa = isa_dict["isa"]
    isa_class = ISA_MAPPING.get(isa, None)
    if isa_class is None:
        raise ValueError("Unknown entry in project file: %s" % isa)
    return isa_class(identifier, isa_dict)
