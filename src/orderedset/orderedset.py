import collections
import weakref

class OrderedSetEntry(object):
    def __init__(self, *args, **kwargs):
        self.prev = kwargs.get("prev", None)
        self.key = kwargs.get("key", None)
        self._set_next(kwargs.get("next", None))

    @property
    def prev(self):
        if self._ref_prev is None:
            return None
        else:
            value = self._ref_prev()
            return value

    @prev.setter
    def prev(self, value):
        if value is None:
            self._ref_prev = None
        else:
            self._ref_prev = weakref.ref(value)

    @property
    def next(self):
        if self._ref_next is None:
            return None
        else:
            value = self._ref_next()
            return value

    def _set_next(self, value):
        if value is None:
            self._ref_next = None
        else:
            self._ref_next = weakref.ref(value)

    @next.setter
    def next(self, value):
        self._set_next(value)

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.clear()

        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            cur = OrderedSetEntry(prev=self.end.prev, key=key, next=self.end)
            self.map[key] = cur

            self.end.prev.next = cur
            self.end.prev = cur

    def clear(self):
        self.end = OrderedSetEntry()
        self.start = OrderedSetEntry()

        self.start.key = None
        self.end.key = None

        self.start.next = self.end
        self.end.prev = self.start

        self.map = {}

    def discard(self, key):
        if key in self.map:        
            entry = self.map.pop(key)
            prev = entry.prev
            next = entry.next

            prev.next = entry.next
            next.prev = entry.prev

    def __iter__(self):
        end = self.end
        cur = self.start.next
        while not cur is end:
            yield cur.key
            cur = cur.next

    def __reversed__(self):
        start = self.start
        cur = self.end.prev
        while not cur is start:
            yield cur.key
            cur = cur.prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
