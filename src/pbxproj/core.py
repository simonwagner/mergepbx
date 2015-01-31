class DictionaryBoundObject(object):
    def __init__(self, dict, restricted_to_keys=None):
        self._dict = dict
        assert self._dict != None
        self._restricted_to_keys = set(restricted_to_keys) if restricted_to_keys != None else None

    def __getattr__(self, attr):
        if not attr.startswith("_") and self._can_access(attr):
            return self._dict[attr]
        else:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if not attr.startswith("_") and attr in self._dict and self._can_access(attr):
            self._dict[attr] = value
        else:
            return super(DictionaryBoundObject, self).__setattr__(attr, value)

    def _get_dict(self):
        return self._dict

    def iterkeys():
        return self._dict.iterkeys()

    def has_attr(self, attr):
        return attr in self._dict

    def get_attr(self, attr, default=Ellipsis):
        if self.has_attr(attr):
            return self.get_attr(attr)
        else:
            if default is not Ellipsis:
                return default
            else:
                raise KeyError(attr)

    def _can_access(self, attr):
        return self._restricted_to_keys == None or attr in self._restricted_to_keys
