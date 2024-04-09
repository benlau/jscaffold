from unittest.mock import MagicMock
import uuid
from jscaffold.iounit.applytosource import ApplyToSource
from jscaffold.iounit.envvar import EnvVar
from jscaffold.processor import Processor
import pytest


@pytest.mark.asyncio
async def test_should_ignore_readonly():
    context = MagicMock()
    key = str(uuid.uuid4())
    input = EnvVar(key).readonly()
    context.input = input
    processor = Processor(context)
    await processor(input, ApplyToSource(), "123")
    assert input.read() is None
