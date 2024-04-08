from jscaffold.patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar, SourceMixin


class EnvFileVar(ScaffoldVar, SourceMixin):
    def __init__(self, key, filename):
        super().__init__()
        self.filename = filename
        self._key = key
        self.patcher = PatchAssignment()

    def _get_key(self):
        return self._key

    def _get_id(self):
        return f"EnvFile:{self.filename}:{self.key}"

    def _write(self, value, context=None):
        content = self._read_file_content()
        replaced, _ = self.patcher(
            content if content is not None else "", self.key, value
        )

        file = open(self.filename, "w")
        file.write(replaced)
        file.close()

        if context is not None and context.print is not None:
            context.print(f"Set {self.key}={value} to {self.filename}\n")

    def _read(self, context=None):
        content = self._read_file_content()
        if content is None:
            return None

        _, value = self.patcher(content, self.key)
        return value

    def _read_file_content(self):
        try:
            file = open(self.filename, "r")
            content = file.read()
            file.close()
            self.content = content
        except FileNotFoundError:
            return None
        return content
