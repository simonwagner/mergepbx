from . import coremerge
from . import pbxmerge
from .pbxmerge import get_project_file_merger

def merge_pbxs(base, mine, theirs):
    merger = get_project_file_merger()

    return merger.merge(base, mine, theirs)
