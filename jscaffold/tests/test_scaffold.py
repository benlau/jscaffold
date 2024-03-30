from unittest.mock import Mock
from jscaffold.iounit.envvar import EnvVar
from jscaffold.layout.formlayout import ApplyToSource
from jscaffold.scaffold import Block
from jscaffold.context import Context


def test_scaffold_form_layout():
    context = Context(
        main_layout=Mock(),
        print_line=Mock(),
        clear_output=Mock(),
    )
    delegate = Block(
        context,
    )
    var1 = EnvVar("VAR1")
    var2 = EnvVar("VAR2")

    ret = delegate.ask([var1, var2])

    assert ret["title"] is None
    assert isinstance(ret["layout"].output, ApplyToSource)
