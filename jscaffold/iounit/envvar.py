import os
from .scaffoldvar import ScaffoldVar
from ..context import Context


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    def __init__(self, key, defaults=""):
        super().__init__()
        self.key = key
        self.defaults = defaults

    def get_id(self):
        return f"Env:{self.key}"

    def _write(self, value=None, context: Context = None):
        validaed_value = self.validate(value, self.defaults)
        os.environ[self.key] = validaed_value
        if context is not None and context.print_line is not None:
            context.print_line(f"Set {self.key}={value}\n")

    def _read(self, context: Context = None):
        return os.getenv(self.key)
