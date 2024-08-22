from contextvars import Context
from .iounit import IOAble
from .format import Format, Formatable, Formatter
import copy


class Valuable(IOAble, Formatable):
    shared_storage = {}

    def __init__(self):
        self.format = Format()

    def copy(self):
        return copy.deepcopy(self)

    def write(self, value=None, context: Context = None):
        super().write(value, context=context)
        id = self._get_id()
        Valuable.shared_storage[id] = value

    def refresh(self, context=None):
        self._has_cached_value = True
        latest = self._read(context=context)
        latest = Formatter(self.format, latest).if_none_use_defaults().value
        id = self._get_id()
        Valuable.shared_storage[id] = latest
        return self

    def update(self, value, context=None):
        self.write(value, context=context)
        id = self._get_id()
        Valuable.shared_storage[id] = value
        return self

    @property
    def value(self):
        # value should not be writable
        id = self._get_id()
        if id not in Valuable.shared_storage:
            self.refresh()
        return Valuable.shared_storage[id] if id in Valuable.shared_storage else None
