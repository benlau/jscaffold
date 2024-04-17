from jscaffold.services.changedispatcher import ChangeDispatcher
from unittest.mock import Mock
import pytest
import asyncio


@pytest.mark.asyncio
async def test_listen():
    listener = Mock()
    dispatcher = ChangeDispatcher()
    dispatcher.add_listener(listener)
    dispatcher.dispatch("test", "payload")
    await asyncio.sleep(0.1)
    listener.assert_called_with("test", "payload")
