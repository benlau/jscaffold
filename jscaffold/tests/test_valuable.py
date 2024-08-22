from jscaffold import Var


def test_valuable_should_share_value(request):
    key = request.node.name
    var1 = Var(key)
    var2 = Var(key)

    var1.update("test")
    assert var2.value == "test"

    var1.update("test2")
    assert var2.value == "test2"
