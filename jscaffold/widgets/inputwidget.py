from enum import Enum
from jscaffold.iounit.iounit import InputUnit
from jscaffold.services.tkservice import tk_serivce
from ipywidgets import widgets
import tempfile
import os
from pathlib import Path


class InputWidgetType(Enum):
    Text = "text"
    Select = "select"
    Textarea = "textarea"
    UploadFile = "upload_file"


class InputWidget:
    def __init__(self, type):
        self.type = type
        self.widget = None

    def focus(self):
        if self.widget is not None:
            self.widget.focus()

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, _value):
        raise NotImplementedError


class TextInputWidget(InputWidget):
    def __init__(self, input: InputUnit):
        super().__init__(InputWidgetType.Text.value)
        value = input.read() if input is not None else None
        format = input.format
        placeholder = input._query_defaults()
        if placeholder is None:
            placeholder = ""
        layout = widgets.Layout(width="360px")
        text_widget = widgets.Text(
            value=value,
            layout=layout,
            placeholder=placeholder,
            disabled=format.readonly,
        )
        self.widget = text_widget

    @property
    def value(self):
        return self.widget.value

    @value.setter
    def value(self, value):
        self.widget.value = value


DEFAULT_ROW_COUNT = 5


class TextAreaInputWidget(InputWidget):
    def __init__(self, input: InputUnit):
        super().__init__(InputWidgetType.Textarea.value)
        value = input.read()
        placeholder = input._query_defaults()
        if placeholder is None:
            placeholder = ""
        format = input.format
        rows = (
            format.multiline
            if not isinstance(format.multiline, bool)
            else DEFAULT_ROW_COUNT
        )
        layout = widgets.Layout(width="360px")
        textarea = widgets.Textarea(
            value=value,
            rows=rows,
            placeholder=placeholder,
            layout=layout,
            disabled=format.readonly,
        )
        self.widget = textarea

    @property
    def value(self):
        return self.widget.value

    @value.setter
    def value(self, value):
        self.widget.value = value


class SelectInputWidget(InputWidget):
    def __init__(self, input: InputUnit):
        super().__init__(InputWidgetType.Select.value)
        value = input.read()
        format = input.format
        self.format = format
        if value not in format.select:
            if input.defaults in format.select:
                value = input.defaults
            else:
                value = None
        select_widget = widgets.Select(
            options=format.select, value=value, disabled=format.readonly
        )
        self.widget = select_widget

    @property
    def value(self):
        return self.widget.value

    @value.setter
    def value(self, value):
        if value not in self.format.select:
            value = None
        self.widget.value = value


class FileUploadInputWidget(InputWidget):
    def __init__(self, input: InputUnit):
        super().__init__(InputWidgetType.UploadFile.value)
        value = str(input) if input is not None else None

        format = input.format
        text_box = widgets.Text(
            value=value, layout=widgets.Layout(width="300px"), disabled=format.readonly
        )
        uploader = widgets.FileUpload(multiple=False)
        self.text_box = text_box
        self.widget = widgets.HBox([text_box, uploader])

        def get_upload_folder():
            if format.upload_folder is not None:
                return format.upload_folder
            base_dir = tempfile.mkdtemp()
            if format.mkdir:
                Path(base_dir).mkdir(parents=True, exist_ok=True)
            return base_dir

        def on_upload_change(change):
            if change["type"] == "change" and change["name"] == "value":
                (file_dict,) = uploader.value
                # Remarks: type, content, size inside the file_dict
                filename = file_dict["name"]
                base_dir = get_upload_folder()
                abs_path = os.path.join(base_dir, filename)
                named_file = open(abs_path, "wb")
                named_file.write(file_dict["content"])
                named_file.close()
                text_box.value = abs_path

        uploader.observe(on_upload_change, names="value")

    @property
    def value(self):
        return self.text_box.value

    @value.setter
    def value(self, value):
        self.text_box.value = value


class LocalPathInputWidget(InputWidget):
    def __init__(self, input: InputUnit):
        def on_click(_):
            self.browser_button.disabled = True
            file_path = tk_serivce.open_file_dialog(input.format.file_type)
            self.browser_button.disabled = False
            if file_path == "":
                return
            text_box.value = file_path

        super().__init__(InputWidgetType.UploadFile.value)
        value = input.read()
        placeholder = input._query_defaults()
        if placeholder is None:
            placeholder = ""
        text_box = widgets.Text(
            value=value,
            layout=widgets.Layout(width="300px"),
            placeholder=placeholder,
            disabled=format.readonly,
        )
        browse_button = widgets.Button(description="Browse", disabled=format.readonly)
        self.text_box = text_box
        self.browser_button = browse_button
        self.widget = widgets.HBox([text_box, browse_button])
        browse_button.on_click(on_click)

    @property
    def value(self):
        return self.text_box.value

    @value.setter
    def value(self, value):
        self.text_box.value = value
