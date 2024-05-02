import os

from jscaffold.iounit.format import Formatter
from .valuable import Valuable
from ..contexts.context import Context


class EnvVar(Valuable):
    """
    Wrapper for environment variable
    """

    def __init__(self, key):
        super().__init__()
        self._key = key

    def _get_key(self):
        return self._key

    def _get_id(self):
        return f"Env:{self.key}"

    def _write(self, value=None, context: Context = None):
        value = (
            Formatter(self.format, value).if_none_use_defaults().cast_to_format().value
        )
        if value is None:
            del os.environ[self.key]
        else:
            os.environ[self.key] = str(value)
        if context is not None and context.log is not None:
            context.log(f"Set {self.key}={self._format_display_value(value)}\n")

    def _read(self, context: Context = None):
        return Formatter(self.format, os.getenv(self.key)).cast_to_format().value
