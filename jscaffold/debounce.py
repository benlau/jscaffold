import asyncio


class KeyFilterDebouncer:
    def __init__(self, delay):
        """Initializes the Debouncer with a specific delay in seconds."""
        self.delay = delay
        self.timer_tasks = {}
        self.tasks = {}
        self.task_id = 0

    def debounce(self, key, func, *args, **kwargs):
        async def run():
            if key in self.timer_tasks:
                self.timer_tasks[key].cancel()  # Cancel the previous task
            try:
                self.timer_tasks[key] = asyncio.get_event_loop().create_task(
                    asyncio.sleep(self.delay)
                )
                await self.timer_tasks[key]
                del self.timer_tasks[key]
                func(*args, **kwargs)
            except asyncio.CancelledError:
                pass

        asyncio.ensure_future(run())

    def __call__(self, key, func, *args, **kwargs):
        self.debounce(key, func, *args, **kwargs)
