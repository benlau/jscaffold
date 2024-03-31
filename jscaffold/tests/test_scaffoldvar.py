from jscaffold.iounit.envvar import EnvVar


def test_value():
    var = EnvVar("VAR1")
    var.write("value")
    assert var.value == "value"


def test_text():
    orig = EnvVar("VAR1")
    assert orig.format.type == "text"
    assert orig.format.multiline is False

    fork = orig.multiline()
    assert fork is orig
    assert orig.format.multiline is True
    assert orig.format.multiline is True


def test_select():
    var = EnvVar("VAR1").select("a", "b", "c")
    assert var.format.select == ["a", "b", "c"]
