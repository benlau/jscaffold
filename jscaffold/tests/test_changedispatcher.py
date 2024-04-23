from unittest import IsolatedAsyncioTestCase
from jscaffold.iounit.envvar import EnvVar
from jscaffold.panel.formpanel import FormPanel
from jscaffold.services.changedispatcher import ChangeDispatcher
from unittest.mock import Mock
import pytest
import asyncio


class TestChangeDispatcher(IsolatedAsyncioTestCase):
    @pytest.mark.asyncio()
    async def test_listen(self):
        listener = Mock()
        dispatcher = ChangeDispatcher()
        dispatcher.add_listener(listener)
        dispatcher.dispatch("test", "payload")
        await asyncio.sleep(0.2)
        listener.assert_called_with("test", "payload")

    @pytest.mark.asyncio()
    async def test_formpanel_submit(self):
        var1 = EnvVar("VAR1")
        callback = Mock()
        form_panel = FormPanel(var1).run(callback)
        form_panel.submit()
        await asyncio.sleep(0)
        callback.assert_called_once()
