from collections import namedtuple, OrderedDict
from orderedset import OrderedSet
from inspect import isclass
import logging

from .coremerge import *
from ..pbxobjects import PBXProjFile

class MergeConflict(object):
    def __init__(self, *args, **kwargs):
        if not "msg" in kwargs:
            raise Exception("msg keyword argument is required for %s" % self.__class__.__name__)
        self.msg = kwargs["msg"]

    def __repr__(self):
        return "<%s: '%s'>" % (self.__class__.__name__, self.msg)

class MergeConflictException(Exception):
    pass

class MergeException(Exception):
    pass

class MergeStrategyManager(object):
    def __init__(self, strategies = {}, *args, **kwargs):
        strategies = dict(strategies)
        strategies.update(kwargs)
        self.strategies = {}

        for key, strategie_class in strategies.iteritems():
            self.strategies[key] = strategie_class(self)

    def get_merger(self, strategy):
        if not strategy in self.strategies:
            raise Exception("strategy not found: %s" % strategy)
        else:
            return self.strategies[strategy]

    def get_project_file_merger(self):
        return self.get_merger("PBXProjectFileMerger3")

class Merger(object):
    def __init__(self, manager):
        self.manager = manager

class _SimpleDictMerger3(Merger):
    IGNORE_CONFLICTS_IN_KEYS = set()

    def __init__(self, manager):
        super(_SimpleDictMerger3, self).__init__(manager)
        self.logger = logging.getLogger()
        self.merging_functions = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and attr_name.startswith("merge_"):
                key = attr_name.replace("merge_", "", 1)
                self.merging_functions[key] = attr

    def merge(self, base, mine, theirs):
        #make a diff for merging
        diff3 = diff3_dict(base, mine, theirs)

        #remove conflicts in ignored keys
        #where we have a special merging function
        for key in self.merging_functions:
            if key in diff3.conflicting:
                diff3.conflicting.remove(key)

        #test if we still have conflicts after removing all keys
        #that have an auto_merge function
        if len(diff3.conflicting) > 0:
            result = self.handle_conflicts(base, mine, theirs, diff3)
        else:
            result = merge_dict(diff3, base, mine, theirs)

        assert(result != None)
        #resolve conflicts with the declared auto merge functions
        result = self.auto_merge(base, mine, theirs, result, diff3)

        assert(result != None)

        #in the end, sort result
        result = merge_key_order(result, base, mine, theirs)

        return result

    def auto_merge(self, base, mine, theirs, result, diff3):
        for name, function in self.merging_functions.iteritems():
            result = function(base, mine, theirs, result, diff3)
        return result

    def handle_conflicts(self, base, mine, theirs, diff3):
        raise MergeConflictException("conflict while merging with %s merger" % self.__class__.__name__)

def create_auto_merge_set(attribute, optional = False):
    def auto_merge_set(self, base, mine, theirs, result, diff3):
        if optional and (False, False, False) == (attribute in base, attribute in mine, attribute in theirs):
            return result

        values = _get_3(attribute, base, mine, theirs, optional = optional, replace_value = ())

        values = Value3(*(OrderedSet(v) for v in values)) #convert to OrderedSet

        values_diff = diff3_set(OrderedSet(values.base), OrderedSet(values.mine), OrderedSet(values.theirs))
        result[attribute] = tuple(merge_ordered_set(values_diff, values.base, values.mine, values.theirs))

        return result

    return auto_merge_set

def create_auto_merge_dict(attribute, optional = False):
    def auto_merge_dict(self, base, mine, theirs, result, diff3):
        if optional and (False, False, False) == (attribute in base, attribute in mine, attribute in theirs):
            return result

        values = _get_3(attribute, base, mine, theirs, optional = optional, replace_value = {})

        values_diff = diff3_dict(values.base, values.mine, values.theirs)

        if len(values_diff.conflicting) > 0:
            raise MergeException("can't merge %s, conflicting values in dictionary: %r" % (attribute, values_diff.conflicting))
        result[attribute] = merge_ordered_dict(values_diff, values.base, values.mine, values.theirs)

        return result

    return auto_merge_dict

class PBXProjectFileMerger3(Merger):
    SUPPORTED_ARCHIVE_VERSIONS = set((1,))
    SUPPORTED_OBJECT_VERSIONS = set((46,))

    def merge(self, base, mine, theirs):
        result = OrderedDict()

        #check if the encoding for all project is
        #the same, otherwise abort
        if base.get_encoding() != theirs.get_encoding() or base.get_encoding() != mine.get_encoding():
            raise ValueError("merging projects with different encoding (base=%s, mine=%s, theirs=%s) is not supported." % (base.get_encoding(), mine.get_encoding(), theirs.get_encoding()))
        encoding = mine.get_encoding()
        #use plist for merging
        base, mine, theirs = (base._plist, mine._plist, theirs._plist)

        self.merge_archiveVersion(result, base, mine, theirs)
        self.merge_classes(result, base, mine, theirs)
        self.merge_objectVersion(result, base, mine, theirs)
        self.merge_objects(result, base, mine, theirs)
        self.merge_rootObject(result, base, mine, theirs)

        return PBXProjFile(result, encoding=encoding)

    def merge_archiveVersion(self, result, base, mine, theirs):
        archiveVersion = _get_3("archiveVersion", base, mine, theirs)
        if not archiveVersion.base == archiveVersion.mine or not archiveVersion.base == archiveVersion.theirs:
            raise MergeException("can not merge projects with different archiveVersion")
        if not int(archiveVersion.base) in self.SUPPORTED_ARCHIVE_VERSIONS:
            raise MergeException("can not merge projects with archiveVersion %s" % archiveVersion.base)

        result["archiveVersion"] = archiveVersion.base

    def merge_classes(self, result, base, mine, theirs):
        classes = _get_3("classes", base, mine, theirs)

        if tuple(len(d) for d in classes) == (0,0,0):
            result["classes"] = {}
        else:
            raise MergeException("merging classes in pbxproj not supported")

    def merge_objectVersion(self, result, base, mine, theirs):
        objectVersion = _get_3("objectVersion", base, mine, theirs)
        if not objectVersion.base == objectVersion.mine or not objectVersion.base == objectVersion.theirs:
            raise MergeException("can not merge projects with different objectVersion")
        if not int(objectVersion.base) in self.SUPPORTED_OBJECT_VERSIONS:
            raise MergeException("can not merge projects with objectVersion %s" % objectVersion.base)

        result["objectVersion"] = objectVersion.base

    def merge_objects(self, result, base, mine, theirs):
        base_objs, mine_objs, theirs_objs = _get_3("objects", base, mine, theirs)

        diff_obj_keys = diff3_dict_keys(base_objs, mine_objs, theirs_objs)

        merged_objects = {}
        #add objects that are new
        for added_object_key in diff_obj_keys.mine_added:
            merged_objects[added_object_key] = mine_objs[added_object_key]
        for added_object_key in diff_obj_keys.theirs_added:
            merged_objects[added_object_key] = theirs_objs[added_object_key]
        #for deleted objects, simply do not add them

        #for common objects we will have to merge
        for common_object_key in diff_obj_keys.common:
            mine_obj_isa = mine_objs[common_object_key]["isa"]

            base_obj, mine_obj, theirs_obj = _get_3(common_object_key, base_objs, mine_objs, theirs_objs, optional = True, replace_value = {"isa" : mine_obj_isa})
            base_isa, mine_isa, theirs_isa = _get_3("isa", base_obj, mine_obj, theirs_obj)

            if not base_isa == mine_isa or not base_isa == theirs_isa:
                raise MergeException("can't merge objects whose ISA has changed. %s %s, %s, %s" %(common_object_key, base_isa, mine_isa, theirs_isa))

            merger_name = base_isa + "Merger3"

            merger = self.manager.get_merger(merger_name)

            merged_obj = merger.merge(base_obj, mine_obj, theirs_obj)
            merged_objects[common_object_key] = merged_obj

        result["objects"] = merge_key_order(merged_objects, base_objs, mine_objs, theirs_objs)

    def merge_rootObject(self, result, base, mine, theirs):
        if mine["rootObject"] != theirs["rootObject"]:
            raise MergeConflictException("conflict in rootObject, can't handle that")
        else:
            result["rootObject"] = mine["rootObject"]

class _AbstractPBXBuildObjectMerger3(_SimpleDictMerger3):
    merge_files = create_auto_merge_set("files", optional = True)

class PBXBuildFileMerger3(_AbstractPBXBuildObjectMerger3):
    pass

class PBXCopyFilesBuildPhaseMerger3(_AbstractPBXBuildObjectMerger3):
    pass

class PBXFileReferenceMerger3(_SimpleDictMerger3):

    def merge_lastKnownFileType(self, base, mine, theirs, result, diff3):
        #special handling for lastKnownFileType
        base_lastKnownFileType, mine_lastKnownFileType, theirs_lastKnownFileType = _get_3("lastKnownFileType", base, mine, theirs, optional = True, replace_value = "")

        #if lastKnownFileType is nowhere present, do nothing
        if (base_lastKnownFileType, mine_lastKnownFileType, theirs_lastKnownFileType) == ("", "", ""):
            return result

        if not base_lastKnownFileType == mine_lastKnownFileType or not base_lastKnownFileType == theirs_lastKnownFileType:
            #if last known file type is different, well, then we delete it simply and let xcode figure out what it should do
            #if however base is empty, then we set it to a known file type
            if base_lastKnownFileType == "":
                if mine_lastKnownFileType == theirs_lastKnownFileType:
                    lastKnownFileType = mine_lastKnownFileType
                else:
                    lastKnownFileType = ""
            else:
                lastKnownFileType = ""
        else:
            lastKnownFileType = base_lastKnownFileType

        result["lastKnownFileType"] = lastKnownFileType

        return result

class PBXFrameworksBuildPhaseMerger3(_AbstractPBXBuildObjectMerger3):
    pass

class PBXGroupMerger3(_SimpleDictMerger3):
    merge_children = create_auto_merge_set("children")
    def merge_sourceTree(self, base, mine, theirs, result, diff3):
        base_sourceTree, mine_sourceTree, theirs_sourceTree = _get_3("sourceTree", base, mine, theirs)

        if not base_sourceTree == mine_sourceTree or not base_sourceTree == theirs_sourceTree:
            raise MergeException("can't merge PBXGroup whose sourceTree has changed")

        return result

class _AbstractTargetMerger3(_SimpleDictMerger3):
    merge_buildPhases = create_auto_merge_set("buildPhases", optional = True)
    merge_dependencies = create_auto_merge_set("dependencies", optional = True)
    merge_files = create_auto_merge_set("files", optional = True)

class PBXFrameworksBuildPhaseMerger3(_AbstractTargetMerger3):
    pass

class PBXResourcesBuildPhaseMerger3(_AbstractTargetMerger3):
    pass

class PBXLegacyTargetMerger3(_AbstractTargetMerger3):
    pass

class PBXNativeTargetMerger3(_AbstractTargetMerger3):
    pass

class PBXShellScriptBuildPhaseMerger3(_AbstractTargetMerger3):
    merge_buildPhases = create_auto_merge_set("inputPaths", optional = True)
    merge_dependencies = create_auto_merge_set("outputPaths", optional = True)
    merge_files = create_auto_merge_set("files", optional = True)

class PBXReferenceProxyMerger3(_SimpleDictMerger3):
    pass

class PBXContainerItemProxyMerger3(_SimpleDictMerger3):
    pass

class PBXTargetDependencyMerger3(_SimpleDictMerger3):
    pass

class PBXProjectMerger3(_SimpleDictMerger3):
    merge_knownRegions = create_auto_merge_set("knownRegions", optional = True)
    merge_targets = create_auto_merge_set("targets")
    merge_attributes = create_auto_merge_dict("attributes", optional = True)

class PBXSourcesBuildPhaseMerger3(_SimpleDictMerger3):
    merge_files = create_auto_merge_set("files")

class PBXHeadersBuildPhaseMerger3(_SimpleDictMerger3):
    merge_files = create_auto_merge_set("files")

class XCBuildConfigurationMerger3(_SimpleDictMerger3):
    def merge_buildSettings(self, base, mine, theirs, result, diff3):
        attribute = "buildSettings"
        values = _get_3(attribute, base, mine, theirs)

        values_diff = diff3_dict(values.base, values.mine, values.theirs)

        resolved_conflicts = {}
        for conflict in values_diff.conflicting:
            #check if conflict happens with a tuple or another list-like type
            for value in values:
                if not conflict in value:
                    continue
                dict_value = value[conflict]
                if not isinstance(dict_value, (tuple, list, set, OrderedSet)):
                    raise MergeException("can't merge %s, conflicting values in dictionary: %r" % (attribute, values_diff.conflicting))
            #ok, we now can merge it with merge_ordered_set as we are sure that it is a tuple or something like that
            #and we assume that items are unique
            dict_values = Value3(values.base[conflict], values.mine[conflict], values.theirs[conflict])

            dict_values_diff = diff3_set(OrderedSet(dict_values.base), OrderedSet(dict_values.mines), OrderedSet(dict_values.theirs))
            resolved_conflicts[conflict] = tuple(merge_ordered_set(dict_values_diff, dict_values.base, dict_values.mines, dict_values.theirs))

            values_diff.conflicting.remove(conflict) #mark as merged

        result[attribute] = merge_ordered_dict(values_diff, values.base, values.mine, values.theirs)
        for conflict, resolution in resolved_conflicts.iteritems():
            result[attribute] = resolution

        return result

class XCConfigurationListMerger3(_SimpleDictMerger3):
    merge_buildConfigurations = create_auto_merge_set("buildConfigurations")

class PBXVariantGroupMerger3(_SimpleDictMerger3):
    merge_children = create_auto_merge_set("children")

class XCVersionGroupMerger3(_SimpleDictMerger3):
    merge_files = create_auto_merge_set("children")

Value3 = namedtuple("Value3", ("base", "mine", "theirs"))

def _get_3(key, base, mine, theirs, optional = False, replace_value = None):
    if not optional:
        get = lambda d, key: d[key]
    else:
        get = lambda d, key, replace_value=replace_value: d.get(key, replace_value)

    base_value = get(base, key)
    mine_value = get(mine, key)
    theirs_value = get(theirs, key)

    return Value3(base_value, mine_value, theirs_value)

def _find_merger(vars):
    classes = ((clazz.__name__, clazz) for varname, clazz in vars.iteritems() if isclass(clazz))
    merger_classes = ((name, clazz) for name, clazz in classes if issubclass(clazz, Merger) and name != "Merger")
    public_classes = ((name, clazz) for name, clazz in merger_classes if not name.startswith("_"))

    return dict(public_classes)

MERGER_MAPPING = _find_merger(dict(locals()))

DEFAULT_MERGE_STRATEGY_MANAGER = MergeStrategyManager(MERGER_MAPPING)

def get_project_file_merger():
    return DEFAULT_MERGE_STRATEGY_MANAGER.get_project_file_merger()
