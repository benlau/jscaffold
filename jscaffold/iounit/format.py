from enum import Enum
from typing import List, Optional, Union


class FormatType(Enum):
    Text = "text"
    File = "file"


class FileSource(Enum):
    Upload = "upload"
    Local = "local"


class Format:
    def __init__(
        self,
        type=FormatType.Text.value,
        multiline: Optional[Union[bool, int]] = False,
        select: Optional[List[str]] = None,
        file_source: FileSource = None,
        upload_folder: str = None,
    ):
        self.type = type
        self.multiline = multiline
        self.select = select
        self.file_source = file_source
        self.upload_folder = upload_folder
