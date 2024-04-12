import os
from .variable import Variable
from ..context import Context


class EnvVar(Variable):
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
        validated_value = self.validate(value, self.format.defaults)
        if validated_value is None:
            del os.environ[self.key]
        else:
            os.environ[self.key] = validated_value
        if context is not None and context.print is not None:
            context.print(f"Set {self.key}={self._format_display_value(value)}\n")

    def _read(self, context: Context = None):
        return os.getenv(self.key)
