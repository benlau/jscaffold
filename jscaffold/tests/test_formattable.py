from jscaffold.iounit.format import Formattable, Format


class Var(Formattable):
    def __init__(self):
        self.format = Format()


def test_format_select_none():
    var = Var()
    var.select("1", "2")
    assert var.format.select == ["1", "2"]
    var.select()
    assert var.format.select is None
