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
        return ret if ret is not None else ""

    def read(self, context: Context = None) -> Optional[Any]:
        return self._read(context=context)

    def _read(self, context: Context = None) -> Optional[Any]:
        """
        Read the raw value. If the value is not set, return None
        """
        raise NotImplementedError()

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
            payload = {"type": "value_changed", "value": value}
            change_dispatcher.dispatch(object_id, payload)
        return ret

    def _write(self, value=None, context: Context = None):
        raise NotImplementedError()


class IOAble(Inputable, Outputable):
    pass
