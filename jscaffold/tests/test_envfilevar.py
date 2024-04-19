from unittest import TestCase
from unittest.mock import Mock, patch
from jscaffold import EnvFileVar
from tempfile import NamedTemporaryFile


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class TestEnvFileVar(TestCase):
    def test_envfilevar_get_id(self):
        variable = EnvFileVar("A", "./config.env")
        assert variable._get_id() == "EnvFile:./config.env:A"

    def test_envfile_var_read_not_existed_file(self):
        var = EnvFileVar("var", "not_existed_file").defaults("default")
        assert var._read() is None
        assert var.value == "default"

    def test_envfile_var_write_not_existed_file(self):
        tmp_file = NamedTemporaryFile(delete=True)
        filename = tmp_file.name
        tmp_file.close()

        var = EnvFileVar("A", filename)
        var.write("value")

        file = open(tmp_file.name, "r")
        content = file.read()

        assert content == "\nA=value"

    def test_source(self):
        with EnvFileVar.source("config.env") as source:
            var1 = source.var("A")
            assert var1.filename == "config.env"

            var2 = source("B")
            assert var2.filename == "config.env"

    def test_copy(self):
        a = EnvFileVar("A", "config.env")
        a.defaults("default")
        b = a.copy()

        assert b.key == "A"
        assert b.filename == "config.env"
        assert b.format.defaults == "default"

        b.defaults("new_default")
        assert a.format.defaults == "default"
