from unittest import TestCase
from unittest.mock import patch
from jscaffold.iounit.envvar import EnvVar
from jscaffold.iounit.format import Formatable, Format, Formatter
import os


class Var(Formatable):
    def __init__(self):
        self.format = Format()


class TestFormatable(TestCase):
    def test_format_select_none(self):
        var = Var()
        var.select("1", "2")
        assert var.format.select == ["1", "2"]
        var.select()
        assert var.format.select is None

    def test_format_defaults_number(self):
        os.environ.pop("VAR", None)
        var = EnvVar("VAR").defaults(1).refresh()
        # It read from defaults and that is why it become 1 instead of "1"
        assert var.value == 1

    @patch("jscaffold.services.changedispatcher.change_dispatcher.dispatch")
    def test_formatable_should_dispatch_change(self, mock_dispatch):
        EnvVar("VAR").select("1", "2")

        mock_dispatch.assert_called_once_with(
            "Env:VAR",
            {"type": "format_changed", "field": "select", "value": ["1", "2"]},
        )


class TestFormatter(TestCase):
    def test_cast_to_format_numer(self):
        var = Var()
        var.number()
        assert Formatter(var.format, "1").cast_to_format().value == 1.0
        assert Formatter(var.format, None).cast_to_format().value is None

    def test_cast_to_format_text(self):
        var = Var()
        assert Formatter(var.format, "1").cast_to_format().value == "1"
        assert Formatter(var.format, None).cast_to_format().value is None
        assert Formatter(var.format, 1.0).cast_to_format().value == "1"
