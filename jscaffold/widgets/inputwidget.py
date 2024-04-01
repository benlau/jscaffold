from enum import Enum
from jscaffold.iounit.iounit import InputUnit
from ipywidgets import widgets
import tempfile
import os


class InputWidgetType(Enum):
    Text = "text"
    Select = "select"
    Textarea = "textarea"
    TempFilePicker = "tmp_file_picker"


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
        value = str(input) if input is not None else None

        layout = widgets.Layout(width="360px")
        text_box = widgets.Text(value=value, layout=layout)
        self.widget = text_box

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
        value = str(input) if input is not None else None

        rows = (
            format.multiline
            if not isinstance(format.multiline, bool)
            else DEFAULT_ROW_COUNT
        )

        textarea = widgets.Textarea(value=value, rows=rows)
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
        value = str(input) if input is not None else None
        format = input.format
        self.format = format
        if value not in format.select:
            if input.defaults in format.select:
                value = input.defaults
            else:
                value = None
        select_widget = widgets.Select(options=format.select, value=value)
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
        super().__init__(InputWidgetType.TempFilePicker.value)
        value = str(input) if input is not None else None

        format = input.format
        text_box = widgets.Text(value=value, layout=widgets.Layout(width="300px"))
        uploader = widgets.FileUpload(multiple=False)
        self.text_box = text_box
        self.widget = widgets.HBox([text_box, uploader], width="360px")

        def get_upload_folder():
            if format.upload_folder is not None:
                return format.upload_folder
            with tempfile.TemporaryDirectory() as temp_dir:
                base_dir = temp_dir
            return base_dir

        def on_upload_change(change):
            if change["type"] == "change" and change["name"] == "value":
                (file_dict,) = uploader.value
                # Remarks: type, content, size inside the file_dict
                filename = file_dict["name"]
                base_dir = get_upload_folder()
                os.mkdir(base_dir)
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
