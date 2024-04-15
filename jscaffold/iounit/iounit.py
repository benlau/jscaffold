from typing import Any, Optional
from abc import ABC
from ..contexts.context import Context
from jscaffold.services.changedispatcher import change_dispatcher


class Inputable(ABC):
    """
    Inputable is a class that represents an input unit.
    """

    def __str__(self):
        return self.to_string()

    def to_string(self, context: Context = None) -> str:
        ret = self._read(context=context)
        ret = self._normalize_read_value(ret)
        return ret if ret is not None else ""

    def read(self, context: Context = None) -> Optional[Any]:
        return self._read(context=context)

    def _read(self, context: Context = None) -> Optional[Any]:
        """
        Read the raw value. If the value is not set, return None
        """
        raise NotImplementedError()

    def _normalize_read_value(self, read_value):
        """
        Normalize the read value
        """
        if read_value is not None:
            return read_value
        if self.format.defaults is not None:
            return self._query_defaults()
        return None

    def _query_defaults(self):
        """
        Query the default value
        """
        defaults = self.format.defaults
        ret = None
        if isinstance(defaults, list):
            ret = defaults[0]
        else:
            ret = defaults

        return ret

    @property
    def id(self):
        return self._get_id()

    @property
    def key(self):
        return self._get_key()

    def _get_key(self):
        raise NotImplementedError()

    def _get_id(self):
        raise NotImplementedError()


class Outputable(ABC):
    def __call__(self, value=None, context: Context = None):
        return self.write(value, context=context)

    def write(self, value=None, context: Context = None):
        ret = self._write(value, context=context)
        if isinstance(self, Inputable):
            object_id = self._get_id()
            change_dispatcher.dispatch(object_id, value)
        return ret

    def _write(self, value=None, context: Context = None):
        raise NotImplementedError()


class IOAble(Inputable, Outputable):
    def if_none_write_default(self):
        """
        If the current value is none, read the value.
        If it is also none, write default
        """
        if self.format.defaults is None:
            return

        value = self._read()
        if value is None:
            self.write(self._query_defaults())
