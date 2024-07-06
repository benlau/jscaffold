from contextlib import contextmanager
from jscaffold.iounit.valuable import Valuable
from jscaffold.patchers.block import PatchBlock


class BlockInFileVar(Valuable):
    default_filename = None

    def __init__(self, key, filename=None):
        super().__init__()
        self.filename = filename
        if filename is not None:
            self.filename = filename
        elif BlockInFileVar.default_filename is not None:
            self.filename = BlockInFileVar.default_filename
        else:
            raise ValueError("filename is not provided")

        self._key = key
        if isinstance(key, str):
            self.patcher = PatchBlock(key, key)
        else:
            self.patcher = PatchBlock(key[0], key[1])
        self.content = None

    def _get_key(self):
        return self._key

    def _get_id(self):
        return f"BlockInFile:{self.filename}:{self.key}"

    def _write(self, value, context=None):
        content = self._read_file_content()
        replaced = self.patcher.write(content if content is not None else "", value)

        file = open(self.filename, "w")
        file.write(replaced)
        file.close()

        if context is not None and context.log is not None:
            context.log(
                f"Set {self.key}={self._format_display_value(value)} to {self.filename}\n"
            )

    def _read(self, context=None):
        content = self._read_file_content()
        if content is None:
            return None

        value = self.patcher.read(content)
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

    @classmethod
    @contextmanager
    def use(cls, filename: str):
        try:
            BlockInFileVar.default_filename = filename
            yield
        finally:
            BlockInFileVar.default_filename = None
