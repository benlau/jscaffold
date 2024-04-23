from unittest.mock import MagicMock
from unittest import IsolatedAsyncioTestCase
from jscaffold.debounce import KeyFilterDebouncer
import asyncio


class TestKeyFilterDebouncer(IsolatedAsyncioTestCase):
    async def test_rapid_successive_calls(self):
        debouncer = KeyFilterDebouncer(0.1)
        mock = MagicMock()

        def func(value):
            mock(value)

        async def rapid_calls():
            debouncer("start", func, "start")
            for _ in range(5):
                debouncer("rapid", func, "rapid")
                await asyncio.sleep(0)
            await asyncio.sleep(0.2)

        asyncio.create_task(rapid_calls())
        await asyncio.sleep(0.3)
        mock.assert_any_call("rapid")
        mock.assert_any_call("start")
        self.assertEqual(mock.call_count, 2)  # "start" and last "rapid"
