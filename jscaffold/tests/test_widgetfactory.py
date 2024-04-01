from jscaffold.iounit.envvar import EnvVar
from jscaffold.widgets.widgetfactory import WidgetFactory


def test_widgetfactory_create_input_with_select():
    factory = WidgetFactory()
    var = EnvVar("VAR").select("A", "B", "C")
    input_widget = factory.create_input(var)
    assert input_widget.widget.value is None
    assert input_widget.widget.options == ("A", "B", "C")

    input_widget.value = "B"

    assert input_widget.widget.value == "B"
    assert input_widget.widget.options == ("A", "B", "C")

    input_widget.value = "value-non-existed"
    assert input_widget.widget.value is None
    assert input_widget.widget.options == ("A", "B", "C")


def test_widgetfactory_create_input_tmp_file():
    factory = WidgetFactory()
    var = EnvVar("VAR").upload_file()
    input_widget = factory.create_input(var)
    assert input_widget.type == "tmp_file_picker"
