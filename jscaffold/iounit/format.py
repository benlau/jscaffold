from enum import Enum
from typing import Any, List, Optional, Union


class FormatType(Enum):
    Text = "text"
    File = "file"


class FileSource(Enum):
    Upload = "upload"
    Local = "local"


class FileType(Enum):
    File = "file"
    Directory = "directory"


class Format:
    def __init__(
        self,
        type=FormatType.Text.value,
        defaults: Any = None,
        readonly: bool = False,
        desc: str = None,
        # For text
        multiline: Optional[Union[bool, int]] = False,
        select: Optional[List[str]] = None,
        password: bool = False,
        # For file
        mkdir: bool = True,
        file_source: FileSource = None,
        upload_folder: str = None,
        file_type: FileType = FileType.File,
    ):
        self.type = type
        self.readonly = readonly
        self.defaults = defaults
        self.password = password
        self.desc = desc

        self.multiline = multiline
        self.select = select
        self.file_source = file_source

        # The folder to upload files to, if it is not
        # set, it will use a temp folder
        self.upload_folder = upload_folder
        self.file_type = file_type
        self.mkdir = mkdir


class Formattable:
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

    def desc(self, value):
        self.format.desc = value
        return self
