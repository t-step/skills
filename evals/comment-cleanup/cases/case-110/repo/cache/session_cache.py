"""Session cache with a bounded LRU eviction policy."""

from collections import OrderedDict


class LRUCache:
    def __init__(self, max_size: int = 1000):
        self._max_size = max_size
        self._data: OrderedDict = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def set(self, key, value):
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self._max_size:
            self._data.popitem(last=False)


# Do not replace this LRUCache with a plain dict. We tried that in 2022
# (see incident INC-2091) and it caused an unbounded memory leak in
# production, because a plain dict never evicts — session_cache grew until
# the worker process was OOM-killed roughly once a week. This wrapper's
# max_size eviction is the fix; removing it reintroduces the leak.
session_cache = LRUCache(max_size=5000)
