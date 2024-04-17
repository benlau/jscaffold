import asyncio


class ChangeDispatcher:
    def __init__(self):
        # It can't use WeakSet because it will be removed in Jupyter environment
        self.listeners = set()
        self.queue = []

    def add_listener(self, listener):
        self.listeners.add(listener)

    def dispatch(self, key, payload):
        async def dispatch_async():
            for item in self.queue:
                for listener in self.listeners:
                    try:
                        listener(*item)
                    except Exception:
                        self.listeners.remove(listener)
            self.queue.clear()

        self.queue.append((key, payload))
        asyncio.create_task(dispatch_async())


class Listener:
    def __init__(self, type, callback):
        self.type = type
        self.callback = callback

    def __call__(self, type, payload):
        if self.type == type:
            self.callback(payload)


change_dispatcher = ChangeDispatcher()
