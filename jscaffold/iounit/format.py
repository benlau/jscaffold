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
        # For text
        multiline: Optional[Union[bool, int]] = False,
        select: Optional[List[str]] = None,
        # For file
        mkdir: bool = True,
        file_source: FileSource = None,
        upload_folder: str = None,
        file_type: FileType = FileType.File,
    ):
        self.type = type
        self.readonly = readonly
        self.defaults = defaults

        self.multiline = multiline
        self.select = select
        self.file_source = file_source

        # The folder to upload files to, if it is not
        # set, it will use a temp folder
        self.upload_folder = upload_folder
        self.file_type = file_type
        self.mkdir = mkdir
