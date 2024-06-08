from contextvars import Context
from .iounit import IOAble
from .format import Format, Formattable, Formatter
import copy


class Valuable(IOAble, Formattable):
    def __init__(self):
        self.format = Format()
        self._has_cached_value = False
        self._cached_value = None

    def copy(self):
        return copy.deepcopy(self)

    def write(self, value=None, context: Context = None):
        super().write(value, context=context)
        self._has_cached_value = True
        self._cached_value = value

    def refresh(self, context=None):
        self._has_cached_value = True
        latest = self._read(context=context)
        latest = Formatter(self.format, latest).if_none_use_defaults().value
        self._cached_value = latest
        return self

    def update(self, value, context=None):
        self.write(value, context=context)
        self._has_cached_value = True
        self._cached_value = value
        return self

    @property
    def value(self):
        # value should not be writable
        if not self._has_cached_value:
            self.refresh()
        return self._cached_value
