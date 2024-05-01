from unittest import TestCase
from jscaffold.iounit.envvar import EnvVar
from jscaffold.iounit.format import Formattable, Format, Formatter
import os


class Var(Formattable):
    def __init__(self):
        self.format = Format()


class TestFormattable(TestCase):
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
