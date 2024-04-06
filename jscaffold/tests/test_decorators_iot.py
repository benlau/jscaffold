from unittest.mock import MagicMock
from jscaffold.decorators.iot import preset_iot
from jscaffold.iounit.sharedstoragevar import SharedStorageVar


def test_iot_preset_should_change_str_to_shared_storage_var():
    res = MagicMock()

    @preset_iot
    def func(
        input=None,
        output=None,
        title=None,
    ):
        res(input)

    func("input")

    inputs = res.call_args_list[0][0]
    input = inputs[0]
    assert isinstance(input, SharedStorageVar) is True
    assert input.key == "input"
