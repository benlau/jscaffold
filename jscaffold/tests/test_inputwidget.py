import uuid
from jscaffold.iounit.envvar import EnvVar
from jscaffold.widgets.widgetfactory import WidgetFactory
from jscaffold.widgets.inputwidget import (
    TextInputWidget,
    TextAreaInputWidget,
    SelectInputWidget,
    FileUploadInputWidget,
    LocalPathInputWidget,
)


def test_textinputwidget_placeholder():
    factory = WidgetFactory()

    var = EnvVar(str(uuid.uuid4()))
    input_widget = factory.create_input(var)
    assert input_widget.text_widget.placeholder == ""

    var = EnvVar(str(uuid.uuid4())).defaults("placeholder")
    input_widget = factory.create_input(var)
    assert input_widget.text_widget.placeholder == "placeholder"


def test_create():
    var = EnvVar("var").select([])
    widgets = [
        TextInputWidget,
        TextAreaInputWidget,
        SelectInputWidget,
        FileUploadInputWidget,
        LocalPathInputWidget,
    ]
    for widget in widgets:
        widget(var)
