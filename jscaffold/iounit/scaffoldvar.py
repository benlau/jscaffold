from typing import List, Optional, Union
from .iounit import IOUnit
from .format import FileSource, FormatType, Format


class ScaffoldVar(IOUnit):
    def __init__(self):
        self.format = Format()
        self._has_cached_value = False
        self._cached_value = None

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

    def refresh(self, context=None):
        self._has_cached_value = True
        self._cached_value = self._normalize_read_value(self._read(context=context))
        return self

    def update(self, value, context=None):
        self._write(value, context=context)
        self._cached_value = value
        return self

    @property
    def value(self):
        # value should not be writable
        if not self._has_cached_value:
            self.refresh()
        return self._cached_value

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
        res = []
        for arg in args:
            if isinstance(arg, list):
                res += arg
            else:
                res.append(arg)
        self.format.select = res
        return self

    def upload_file(self, folder: str = None, mkdir: bool = False):
        self.format.type = FormatType.File.value
        self.format.file_source = FileSource.Upload.value
        self.format.upload_folder = folder
        self.format.mkdir = mkdir
        return self

    def local_path(self):
        self.format.type = FormatType.File.value
        self.format.file_source = FileSource.Local.value
        return self
