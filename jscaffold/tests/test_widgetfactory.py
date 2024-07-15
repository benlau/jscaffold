from unittest import TestCase
from jscaffold.iounit.envvar import EnvVar
from jscaffold.iounit.iounit import Inputable
from jscaffold.widgets.widgetfactory import WidgetFactory


class TestWidgetFactory(TestCase):
    def test_widgetfactory_create_input_with_select(self):
        factory = WidgetFactory()
        var = EnvVar("VAR").select("A", "B", "C")
        input_widget = factory.create_input(var)
        assert input_widget.select_widget.value is None
        assert input_widget.select_widget.options == ("A", "B", "C")

        input_widget.value = "B"

        assert input_widget.select_widget.value == "B"
        assert input_widget.select_widget.options == ("A", "B", "C")

        input_widget.value = "value-non-existed"
        assert input_widget.select_widget.value is None
        assert input_widget.select_widget.options == ("A", "B", "C")

    def test_widgetfactory_create_upload_file_input(self):
        factory = WidgetFactory()
        var = EnvVar("VAR").upload_file()
        input_widget = factory.create_input(var)
        assert input_widget.type == "upload_file"

    def test_widgetfactory_create_non_Formatable_input(self):
        class DummyInput(Inputable):
            def _read(self, context=None):
                return "dummy"

        factory = WidgetFactory()
        input = DummyInput()
        factory.create_input(input)
