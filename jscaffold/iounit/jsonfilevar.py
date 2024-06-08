from jscaffold.patchers.dict import PatchDict
from .valuable import Valuable
from contextlib import contextmanager
from collections import OrderedDict
import json


class JsonFileVar(Valuable):
    default_filename = None
    default_indent = None

    class State:
        def __init__(self):
            self.key = None
            self.indent = None
            self.reader = None
            self.path = None

    def __init__(self, key, filename=None):
        super().__init__()
        if filename is not None:
            self.filename = filename
        elif JsonFileVar.default_filename is not None:
            self.filename = JsonFileVar.default_filename
        else:
            raise ValueError("filename is not provided")

        self.patcher = PatchDict()
        self.state = JsonFileVar.State()
        self.state.path = key
        self.state.key = key
        self.state.indent = JsonFileVar.default_indent

    def indent(self, indent):
        self.state.indent = indent
        return self

    def _get_key(self):
        return self.state.key

    def _get_id(self):
        return f"JsonFile:{self.filename}:{self.state.key}"

    def reader(self, value):
        self.state.reader = value
        return self

    def path(self, value):
        self.state.path = value
        return self

    def _write(self, value, context=None):
        content = self._read_json_from_file()
        if content is None:
            content = {}
        new_content = self.patcher.write(content, self.state.path, value)
        with open(self.filename, "w") as file:
            file.write(json.dumps(new_content, indent=self.state.indent))
            file.close()

        if context is not None and context.log is not None:
            context.log(
                f"Set {self.key}={self._format_display_value(value)} to {self.filename}\n"
            )

    def _read(self, context=None):
        content = self._read_json_from_file()
        if content is None:
            return None

        if callable(self.state.reader):
            value = self.state.reader(content)
        else:
            value = self.patcher.read(
                content,
                self.state.reader if self.state.reader is not None else self.state.path,
            )
        if value is None:
            return None
        return value

    def _read_json_from_file(self):
        try:
            with open(self.filename, "r") as file:
                content = file.read()
            json_content = json.loads(content, object_pairs_hook=OrderedDict)
            return json_content
        except FileNotFoundError:
            return None

    @classmethod
    @contextmanager
    def use(cls, filename: str, indent=None):
        try:
            JsonFileVar.default_filename = filename
            JsonFileVar.default_indent = indent
            yield
        finally:
            JsonFileVar.default_filename = None
            JsonFileVar.default_indent = None
