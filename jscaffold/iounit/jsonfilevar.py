from jscaffold.patchers.dict import PatchDict
from .scaffoldvar import ScaffoldVar
from collections import OrderedDict
import json


class JsonFileVar(ScaffoldVar):
    class State:
        def __init__(self):
            self.key = None
            self.indent = None
            self.reader = None

    def __init__(self, key, filename):
        super().__init__()
        self.filename = filename
        self.patcher = PatchDict()
        self.state = JsonFileVar.State()
        self.state.reader = key
        self.state.key = key

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

    def _write(self, value, context=None):
        content = self._read_json_from_file()
        if content is None:
            content = {}
        new_content = self.patcher.write(content, self.state.key, value)
        file = open(self.filename, "w")
        file.write(json.dumps(new_content, indent=self.state.indent))
        file.close()

        if context is not None and context.print is not None:
            context.print(f"Set {self.key}={value} to {self.filename}\n")

    def _read(self, context=None):
        content = self._read_json_from_file()
        if content is None:
            return None

        if callable(self.state.reader):
            value = self.state.reader(content)
        else:
            value = self.patcher.read(content, self.state.reader)
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
