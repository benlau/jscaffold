from jscaffold.iounit.envvar import EnvVar
import os
import uuid
from unittest.mock import patch, Mock
from unittest import TestCase


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class ScaffoldVarTest(TestCase):
    def test_value(self):
        var = EnvVar("VAR1")
        var.write("value")
        assert var.value == "value"

    def test_value_default(self):
        key = str(uuid.uuid4())
        var = EnvVar(key).defaults("default")
        assert var.value == "default"

    def test_write(self):
        """
        It should update the cached value
        """
        key = str(uuid.uuid4())
        var = EnvVar(key).defaults("V1")
        assert var.value == "V1"

        var.write("V2")
        assert var.value == "V2"

    def test_refresh(self):
        var = EnvVar("VAR1")
        os.environ["VAR1"] = "random-value-in-test-value"
        assert var.value == "random-value-in-test-value"

        os.environ["VAR1"] = "random-value-in-test-value2"
        assert var.value == "random-value-in-test-value"

        assert var.refresh().value == "random-value-in-test-value2"

    def test_update(self):
        var = EnvVar("VAR1").refresh()
        os.environ["VAR1"] = str(uuid.uuid4())
        assert var.value != os.environ["VAR1"]
        assert var.update(str(uuid.uuid4())).value == os.environ["VAR1"]

    def test_multiline(self):
        orig = EnvVar("VAR1")
        assert orig.format.type == "text"
        assert orig.format.multiline is False

        fork = orig.multiline()
        assert fork is orig
        assert orig.format.multiline is True
        assert orig.format.multiline is True

    def test_select(self):
        var = EnvVar("VAR1").select("a", "b", "c")
        assert var.format.select == ["a", "b", "c"]

        var = EnvVar("VAR1").select(["a", "b", "c"])
        assert var.format.select == ["a", "b", "c"]
