import uuid
from jscaffold.contexts.context import IOContext
from jscaffold.iounit.envfilevar import EnvFileVar
from jscaffold.iounit.envvar import EnvVar
from jscaffold.processor import Processor
from unittest.mock import MagicMock
import asyncio
import pytest
from tempfile import NamedTemporaryFile
import os


@pytest.mark.asyncio
async def test_processor_skip_options():
    processor = Processor()

    def callback(value):
        assert value == "test"

    await processor(input=None, output=callback, value="test")


@pytest.mark.asyncio
async def test_processor_execute_list():
    callback = MagicMock()
    context = IOContext()
    processor = Processor(context)
    await processor(EnvVar("VAR1"), [callback, callback], "input")

    assert callback.call_count == 2


def test_processor_create_task():
    output = MagicMock()
    processor = Processor()
    done = MagicMock()
    task = processor.create_task(EnvVar("VAR1"), output, "input")
    task.add_done_callback(done)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    done.assert_called_once()


def test_processor_run_script():
    output = """echo Hello"""
    context = MagicMock()
    processor = Processor(context)
    task = processor.create_task(None, output, None)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    context.log.assert_called_once_with("Hello\n")


@pytest.mark.asyncio
async def test_processor_run_script_pass_variable():
    output = """echo $VAR1"""
    context = MagicMock()
    processor = Processor(context)
    tmp_file = NamedTemporaryFile(delete=True)

    var = EnvFileVar("VAR1", tmp_file.name)
    var.write("123")

    await processor(var, output, var.value)
    context.log.assert_called_once_with("123\n")


@pytest.mark.asyncio
async def test_processor_run_script_pass_variable_from_value():
    """
    It should pass the value to the script instead of reading
    from input
    """
    os.environ["VAR1"] = ""
    output = """echo $VAR1"""
    context = MagicMock()
    processor = Processor(context)
    var = EnvVar("VAR1")
    await processor(var, output, "123")
    context.log.assert_called_once_with("123\n")


@pytest.mark.asyncio
async def test_processor_throw_exception():
    """
    It should write the error message to context.log
    """

    def callback():
        raise Exception("Error")

    context = MagicMock()
    processor = Processor(context)
    await processor(None, callback, context)
    context.log.assert_called_once_with("Error")


@pytest.mark.asyncio
async def test_processor_add_apply_to_source():
    """
    It should add the apply method to the source
    if save_changes was set in context
    """
    key = str(uuid.uuid4())
    var = EnvVar(key)
    context = MagicMock()
    context.save_changes = False
    context.input = var
    processor = Processor(context)
    await processor(var, None, "123")
    assert os.environ.get(key) is None

    context.save_changes = True
    processor = Processor(context)
    await processor(var, None, "123")
    assert os.environ.get(key) == "123"


def test_processor_invoke():
    context = IOContext()
    process = Processor(context)
    is_called = False

    def callback(log, value):
        nonlocal is_called
        is_called = True
        assert value == "value"
        assert log == context.log

    process.invoke(callback, "value", context)
    assert is_called is True
