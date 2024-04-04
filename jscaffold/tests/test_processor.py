from jscaffold.iounit.envfilevar import EnvFileVar
from jscaffold.processor import Processor
from unittest.mock import MagicMock
import asyncio
import pytest
from tempfile import NamedTemporaryFile


@pytest.mark.asyncio
async def test_processor_skip_options():
    processor = Processor()

    def callback(value):
        assert value == "test"

    await processor(input=None, output=callback, value="test")


@pytest.mark.asyncio
async def test_processor_execute_list():
    callback = MagicMock()

    processor = Processor()
    await processor("input", [callback, callback], MagicMock())

    assert callback.call_count == 2


def test_processor_create_task():
    output = MagicMock()
    processor = Processor()
    done = MagicMock()
    task = processor.create_task("input", output, MagicMock())
    task.add_done_callback(done)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    done.assert_called_once()


def test_processor_run_script():
    output = """echo 123"""
    context = MagicMock()
    processor = Processor(context)
    task = processor.create_task(None, output, MagicMock())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    context.print_line.assert_called_once_with("123\n")


@pytest.mark.asyncio
async def test_processor_run_script_pass_variable():
    output = """echo $VAR1"""
    context = MagicMock()
    processor = Processor(context)
    tmp_file = NamedTemporaryFile(delete=True)

    var = EnvFileVar("VAR1", tmp_file.name)
    var.write("123")

    await processor(var, output, var.value)
    context.print_line.assert_called_once_with("123\n")
