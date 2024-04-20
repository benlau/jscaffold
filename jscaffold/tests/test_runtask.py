from unittest.mock import MagicMock
from jscaffold.task.runtask import RunTask
import pytest
import threading


@pytest.mark.asyncio()
async def test_runtask_should_print_at_main_thread():
    content = []
    is_main_thread = None

    def print(line):
        content.append(line)
        nonlocal is_main_thread
        is_main_thread = threading.current_thread() is threading.main_thread()

    script = """\
    echo 1
    echo 2
    echo 3
    """

    runtask = RunTask()
    runtask.script = script
    await runtask(print=print)

    assert content == ["1\n", "2\n", "3\n"]
    assert is_main_thread is True


@pytest.mark.asyncio()
async def test_runtask_should_support_env():
    env = {"JS_VALUE": "test"}
    script = "echo $JS_VALUE"
    print = MagicMock()

    runtask = RunTask()
    runtask.script = script
    await runtask(print=print, env=env)
    print.assert_called_once_with("test\n")
