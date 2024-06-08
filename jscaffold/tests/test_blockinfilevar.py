from unittest import TestCase
from unittest.mock import Mock, patch
from jscaffold import BlockInFileVar
from tempfile import NamedTemporaryFile


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class TestBlockInFileVar(TestCase):
    def test_blockinfilevar_get_id(self):
        variable = BlockInFileVar("A", "./config.env")
        assert variable._get_id() == "BlockInFile:./config.env:A"

    def test_blockinfile_var_read_not_existed_file(self):
        var = BlockInFileVar("DIVIDER", "not_existed_file").defaults("default")
        assert var._read() is None
        assert var.value == "default"

    def test_blockinfile_var_write_not_existed_file(self):
        tmp_file = NamedTemporaryFile(delete=True)
        filename = tmp_file.name
        tmp_file.close()

        var = BlockInFileVar("A", filename)
        var.write("value")

        file = open(tmp_file.name, "r")
        content = file.read()

        assert content == "\nA\nvalue\nA"

    def test_use(self):
        with BlockInFileVar.use("config.env"):
            var1 = BlockInFileVar("A")
            assert var1.filename == "config.env"

            var2 = BlockInFileVar("B")
            assert var2.filename == "config.env"

        assert BlockInFileVar.default_filename is None

    def test_copy(self):
        a = BlockInFileVar("A", "config.env")
        a.defaults("default")
        b = a.copy()

        assert b.key == "A"
        assert b.filename == "config.env"
        assert b.format.defaults == "default"

        b.defaults("new_default")
        assert a.format.defaults == "default"
