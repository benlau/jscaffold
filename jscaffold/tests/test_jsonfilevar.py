from unittest import TestCase
from unittest.mock import Mock, patch
from jscaffold.iounit.jsonfilevar import JsonFileVar
from tempfile import NamedTemporaryFile
import json
import textwrap


def write_to_tmp(dict):
    tmp_file = NamedTemporaryFile(delete=False)
    content = json.dumps(dict)
    tmp_file.write(bytes(content, "utf-8"))
    tmp_file.close()
    return tmp_file.name


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class TestJsonFileVar(TestCase):
    def test_jsonfilevar_get_id(self):
        variable = JsonFileVar("A", "./config.json")
        assert variable.id == "JsonFile:./config.json:A"

    def test_jsonfilevar_read_from_file(self):
        source = write_to_tmp({"A": {"B": {"C": "value"}}})
        variable = JsonFileVar("A.B.C", source)
        assert variable.value == "value"

    def test_jsonfilevar_read_boolean_from_file(self):
        source = write_to_tmp({"A": {"B": {"C": True}}})
        variable = JsonFileVar("A.B.C", source)
        assert variable.value is True

    def test_jsonfilevar_write_to_file(self):
        source = write_to_tmp({"A": {"B": {"C": "value"}}})
        variable = JsonFileVar("A.B.C", source).indent(4)
        variable.write("new_value")

        with open(source, "r") as file:
            content = file.read()
            assert content == textwrap.dedent(
                """\
            {
                "A": {
                    "B": {
                        "C": "new_value"
                    }
                }
            }"""
            )

    @patch("builtins.open")
    def test_jsonfilevar_str_reader(self, mock_open):
        json_str = '{"A": {"B": {"C": "value"}}}'
        mock_open.return_value.__enter__().read.return_value = json_str
        var = JsonFileVar("C", "mock-file").reader("A.B.C")
        assert var.value == "value"

    @patch("builtins.open")
    def test_jsonfilevar_func_reader(self, mock_open):
        json_str = '{"A": {"B": {"C": "value"}}}'
        mock_open.return_value.__enter__().read.return_value = json_str

        def query(dict):
            return dict["A"]["B"]["C"]

        var = JsonFileVar("C", "mock-file").reader(query)
        assert var.value == "value"

    @patch("builtins.open")
    def test_jsonfilevar_func_path(self, mock_open):
        json_str = '{"A": {"B": {"C": "value"}}}'
        mock_open.return_value.__enter__().read.return_value = json_str

        var = JsonFileVar("C", "mock-file").path("A.B.C")
        assert var.value == "value"

    @patch("builtins.open")
    def test_jsonfilevar_read_number(self, mock_open):
        json_str = '{"A": {"B": {"C": 1}}}'
        mock_open.return_value.__enter__().read.return_value = json_str

        var = JsonFileVar("C", "mock-file").path("A.B.C")
        assert var.value == 1

    @patch("builtins.open")
    def test_jsonfilevar_write_number(self, mock_open):
        json_str = '{"A": {"B": {"C": 1}}}'
        mock_open.return_value.__enter__().read.return_value = json_str
        var = JsonFileVar("C", "mock-file").path("A.B.C")
        var.update(2)
        mock_open.return_value.__enter__().write.assert_called_with(
            '{"A": {"B": {"C": 2}}}'
        )

    def test_source(self):
        with JsonFileVar.source("config.json", indent=7) as source:
            var1 = source.var("A")
            assert var1.filename == "config.json"
            assert var1.state.indent == 7

            var2 = source("B")
            assert var2.filename == "config.json"
            assert var2.state.indent == 7
