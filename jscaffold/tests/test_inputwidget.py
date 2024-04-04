import uuid
from jscaffold.iounit.envvar import EnvVar
from jscaffold.widgets.widgetfactory import WidgetFactory


def test_textinputwidget_placeholder():
    factory = WidgetFactory()

    var = EnvVar(str(uuid.uuid4()))
    input_widget = factory.create_input(var)
    assert input_widget.widget.placeholder == ""

    var = EnvVar(str(uuid.uuid4())).defaults("placeholder")
    input_widget = factory.create_input(var)
    assert input_widget.widget.placeholder == "placeholder"
