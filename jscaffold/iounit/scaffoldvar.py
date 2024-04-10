from contextlib import contextmanager
from contextvars import Context
from typing import List, Optional, Union
from .iounit import IOUnit
from .format import FileSource, FileType, FormatType, Format
import copy


class ScaffoldVar(IOUnit):
    def __init__(self):
        self.format = Format()
        self._has_cached_value = False
        self._cached_value = None

    def copy(self):
        return copy.deepcopy(self)

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

    def write(self, value=None, context: Context = None):
        super().write(value, context=context)
        self._has_cached_value = True
        self._cached_value = value

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

    def _format_display_value(self, value):
        if self.format.password is True:
            return "*********"
        return value if value is not None else ""

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

    def local_path(self, file_type=FileType.File.value):
        self.format.type = FormatType.File.value
        self.format.file_source = FileSource.Local.value
        self.format.file_type = file_type
        return self

    def readonly(self, value=True):
        self.format.readonly = value
        return self

    def password(self, value=True):
        self.format.password = value
        return self


class SourceMixin:
    @classmethod
    @contextmanager
    def source(cls, filename: str):
        class Source:
            def __init__(self):
                self.filename = filename

            def __call__(self, key):
                return self.var(key)

            def var(self, key):
                return cls(key, self.filename)

        yield Source()
