from jscaffold.iounit.envvar import EnvVar
from jscaffold.widgetfactory import WidgetFactory


def test_widgetfactory_create_select_widget():
    factory = WidgetFactory()
    var = EnvVar("VAR", select=["A", "B", "C"])
    input_widget = factory.create_input(var)
    assert input_widget.widget.value is None
    assert input_widget.widget.options == ("A", "B", "C")

    input_widget.set_value("B")

    assert input_widget.widget.value == "B"
    assert input_widget.widget.options == ("A", "B", "C")

    input_widget.set_value("Value-non-existed")
    assert input_widget.widget.value is None
    assert input_widget.widget.options == ("A", "B", "C")
