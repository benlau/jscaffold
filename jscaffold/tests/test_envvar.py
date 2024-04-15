from jscaffold.iounit.envvar import EnvVar
import os
from unittest.mock import patch


def test_envvar_get_id():
    var = EnvVar("VALUE_NOT_EXISTED")

    assert var._get_id() == "Env:VALUE_NOT_EXISTED"


def test_envvar_defaults_is_array():
    var = EnvVar("VALUE_NOT_EXISTED").defaults(["V1", "V2"])

    assert str(var) == "V1"


def test_envvar_write_without_value():
    name = "7ccb192e-4de4-4720-aa65-e3e687e7a5eb"
    var = EnvVar(name).defaults("default")
    var()

    assert os.getenv(name) == "default"


def test_envvar_write_none():
    var = EnvVar("var1")
    var.write("test")
    var.write(None)

    assert os.getenv("var1", None) is None


@patch("jscaffold.services.changedispatcher.change_dispatcher.dispatch")
def test_envvar_write_should_dispatch_change(mock_dispatch):
    var = EnvVar("VAR")
    var.write("value")

    mock_dispatch.assert_called_once_with("Env:VAR", "value")
