from typing import List, Optional, Union
from .iounit import IOUnit
from .format import FileSource, FormatType, Format


class ScaffoldVar(IOUnit):
    def __init__(self):
        self.format = Format()

    def validate(self, value=None, defaults=None):
        if value is not None:
            return value
        if defaults is None:
            return None

        if isinstance(defaults, str):
            return defaults
        elif isinstance(defaults, list):
            return defaults[0]

        return None

    @property
    def value(self):
        return self.read()

    @value.setter
    def value(self, value):
        self.write(value)

    def defaults(self, value):
        self.format.defaults = value
        return self

    def multiline(self, multiline: Optional[Union[bool, int]] = True):
        self.format.multiline = multiline
        return self

    def select(
        self,
        *args: Optional[List[str]],
    ):
        self.format.select = list(args)
        return self

    def upload_file(self, folder: str = None):
        self.format.type = FormatType.File.value
        self.format.file_source = FileSource.Upload.value
        self.format.upload_folder = folder
        return self
