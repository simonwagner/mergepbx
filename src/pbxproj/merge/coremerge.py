from collections import namedtuple, OrderedDict
from itertools import chain, izip
from orderedset import OrderedSet

KeysDictDiff = namedtuple("KeysDictDiff", ("added", "deleted", "common"))
KeysDictDiff3 = namedtuple("KeysDictDiff", ("mine_added", "theirs_added", "deleted", "common", "conflicting_deleted"))
DictDiff = namedtuple("DictDiff", ("added", "deleted", "updated", "common"))
DictDiff3 = namedtuple("DictDiff3", ("mine_added", "theirs_added", "deleted", "mine_updated", "theirs_updated", "conflicting", "common"))
SetDiff3 = namedtuple("SetDiff3", ("added", "deleted", "common"))

def diff_dict_keys(base, mine):
    base_keys = set(base.iterkeys())
    mine_keys = set(mine.iterkeys())

    added = mine_keys - base_keys
    deleted = base_keys - mine_keys
    common = base_keys & mine_keys

    return KeysDictDiff(added, deleted, common)

def diff3_dict_keys(base, mine, theirs):
    base_keys = set(base.iterkeys())
    mine_keys = set(mine.iterkeys())
    theirs_keys = set(theirs.iterkeys())

    diff_base_with_mine = diff_dict_keys(base, mine)
    diff_base_with_theirs = diff_dict_keys(base, theirs)

    #only the ones which are added exclusivly by mine or theirs
    #can be merged without possible conflicts
    mine_added = diff_base_with_mine.added - diff_base_with_theirs.added
    theirs_added = diff_base_with_theirs.added - diff_base_with_mine.added
    #those which are added by both might contain conflicts in their values
    #those keys will be saved in common later on

    #only the ones which are deleted in both can be savely deleted
    deleted = diff_base_with_mine.deleted & diff_base_with_theirs.deleted
    #keys that are still present in mine or theirs might have been edited
    #and therefore conflict
    conflicting_deleted = (mine_keys & diff_base_with_theirs.deleted) | (theirs_keys & diff_base_with_theirs.deleted)

    #common keys between mine and theirs (includes keys added by both)
    common = (mine_keys & theirs_keys)

    return KeysDictDiff3(mine_added, theirs_added, deleted, common, conflicting_deleted)

def diff_dict(base, mine, test_updated = lambda a,b: a != b):
    keys_diff = diff_dict_keys(base, mine)
    updated_keys = set()
    for key in keys_diff.common:
        if test_updated(base[key], mine[key]):
            updated_keys.add(key)
    common = keys_diff.common - updated_keys
    return DictDiff(added=keys_diff.added, deleted=keys_diff.deleted, updated=updated_keys, common=common)

def diff3_dict(base, mine, theirs, test_updated = lambda a,b: a != b):
    diff_base_with_mine = diff_dict(base, mine, test_updated)
    diff_base_with_theirs = diff_dict(base, theirs, test_updated)
    diff_mine_with_theirs = diff_dict(mine, theirs, test_updated)

    conflicting_update = (diff_base_with_mine.updated & diff_base_with_theirs.updated) - diff_mine_with_theirs.common
    conflicting_added = (diff_base_with_mine.added | diff_base_with_theirs.added) & diff_mine_with_theirs.updated
    conflicting_deleted = (diff_base_with_mine.deleted & diff_base_with_theirs.updated) | (diff_base_with_theirs.deleted & diff_base_with_mine.updated)

    conflicting = conflicting_update | conflicting_added | conflicting_deleted

    mine_added = diff_base_with_mine.added - conflicting
    theirs_added = diff_base_with_theirs.added - conflicting
    deleted = (diff_base_with_theirs.deleted | diff_base_with_mine.deleted) - conflicting
    mine_updated = diff_base_with_mine.updated - conflicting
    theirs_updated = diff_base_with_theirs.updated - conflicting

    common = diff_base_with_mine.common & diff_base_with_theirs.common

    return DictDiff3(mine_added=mine_added, theirs_added=theirs_added, deleted=deleted, mine_updated=mine_updated, theirs_updated=theirs_updated, conflicting=conflicting, common=common)

def diff3_set(base, mine, theirs):
    added = (mine - base) | (theirs - base)
    deleted = set(e for e in base if not e in mine or not e in theirs)
    common = base & mine & theirs

    return SetDiff3(added=added, deleted=deleted, common=common)

def merge_dict(diff, base, mine, theirs):
    assert(len(diff.conflicting) == 0)

    result = {}

    for key in chain(diff.mine_added, diff.mine_updated):
        result[key] = mine[key]
    for key in chain(diff.theirs_added, diff.theirs_updated):
        result[key] = theirs[key]
    for key in diff.common:
        result[key] = mine[key]

    return result

def merge_key_order(result, base, mine, theirs):
    base_keys, mine_keys, theirs_keys = (OrderedSet(k) for k in (base.iterkeys(), mine.iterkeys(), theirs.iterkeys()))

    keys_diff = diff3_set(base_keys, mine_keys, theirs_keys)
    keys_merged = merge_ordered_set(keys_diff, base_keys, mine_keys, theirs_keys)

    result = OrderedDict((key, result[key]) for key in keys_merged)

    return result 

def merge_ordered_dict(diff, base, mine, theirs):
    unordered = merge_dict(diff, base, mine, theirs)
    result = merge_key_order(unordered, base, mine, theirs)

    return result

# merge an ordered so that with the following holds true
# MINE:   m1 - M
#            /   \
# THEIRS: t1 ----> t2
# the result of the merged version of m1 and t1 (which is called M)
# should be the same when merging t1 and M (that means t1 + diff(t1, M) = M)
def merge_ordered_set(diff, base, mine, theirs):
    mine_merged = mine - diff.deleted
    theirs_merged = theirs - diff.deleted
    mine_added = mine_merged - theirs_merged
    merged = OrderedSet()

    theirs_merged_iter = iter(theirs_merged)
    mine_merged_iter = iter(mine_merged)

    for theirs_el in theirs_merged_iter:
        for mine_el in mine_merged_iter:
            if mine_el in mine_added:
                merged.add(mine_el)
            else:
                break
        merged.add(theirs_el)

    for mine_el in mine_merged_iter:
        merged.add(mine_el)

    return merged

def merge_set(diff, base, mine, theirs):
    return diff.common | diff.added
