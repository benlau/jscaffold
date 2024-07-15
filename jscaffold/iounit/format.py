from enum import Enum
from typing import Any, List, Optional, Union
import re
from jscaffold.iounit.iounit import Inputable
from jscaffold.utils import args_to_list
from jscaffold.services.changedispatcher import change_dispatcher


class FormatType(Enum):
    Text = "text"
    File = "file"
    Number = "number"


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


class Formatable:
    def _format_display_value(self, value):
        if self.format.password is True:
            return "*********"
        return value if value is not None else ""

    def _dispatch_format_changed(self, payload: dict):
        if isinstance(self, Inputable):
            object_id = self._get_id()
            change_dispatcher.dispatch(object_id, payload)

    def defaults(self, value):
        self.format.defaults = value
        return self

    def get_defaults(self):
        """
        Get the default value
        """
        defaults = self.format.defaults
        ret = None
        if isinstance(defaults, list):
            ret = defaults[0]
        else:
            ret = defaults

        return ret

    def multiline(self, multiline: Optional[Union[bool, int]] = True):
        self.format.multiline = multiline
        return self

    def select(
        self,
        *args: Optional[List[str]],
    ):
        self.format.select = args_to_list(args, defaults=None)
        self._dispatch_format_changed(
            {"type": "format_changed", "field": "select", "value": self.format.select}
        )
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
        self._dispatch_format_changed(
            {"type": "format_changed", "field": "read_only", "value": value}
        )
        return self

    def password(self, value=True):
        self.format.password = value
        self._dispatch_format_changed(
            {"type": "format_changed", "field": "password", "value": value}
        )
        return self

    def desc(self, value):
        self.format.desc = value
        self._dispatch_format_changed(
            {"type": "format_changed", "field": "read_only", "value": value}
        )
        return self

    def number(self):
        self.format.type = FormatType.Number.value
        self._dispatch_format_changed(
            {"type": "format_changed", "field": "number", "value": None}
        )
        return self


class Formatter:
    def __init__(self, format: Format, value):
        self.format = format
        self.value = value

    def if_none_use_defaults(self):
        defaults = self.format.defaults
        if self.value is not None:
            return self
        if defaults is None:
            return self

        if isinstance(defaults, list):
            self.value = defaults[0]
        else:
            self.value = defaults

        return self

    def cast_to_format(self):
        if self.format.type == FormatType.Number.value:
            self.value = float(self.value) if self.value is not None else None

        if self.format.type == FormatType.Text.value:
            # remove decimal point if it is 0
            if isinstance(self.value, float):
                self.value = str(self.value)
                self.value = re.sub(r"\.0+$", "", self.value)

        return self
