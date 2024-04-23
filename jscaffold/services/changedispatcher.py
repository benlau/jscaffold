from jscaffold.debounce import KeyFilterDebouncer


class ChangeDispatcher:
    def __init__(self):
        # It can't use WeakSet because it will be removed in Jupyter environment
        self.listeners = set()
        self.queue = []
        self.debouncer = KeyFilterDebouncer(0.1)

    def add_listener(self, listener):
        self.listeners.add(listener)

    def dispatch(self, key, payload):
        self.debouncer(key, self._invoke_listeners, key, payload)

    def _invoke_listeners(self, key, payload):
        for listener in self.listeners:
            try:
                listener(key, payload)
            except Exception:
                self.listeners.remove(listener)


class Listener:
    def __init__(self, type, callback):
        self.type = type
        self.callback = callback

    def __call__(self, type, payload):
        if self.type == type:
            self.callback(payload)


change_dispatcher = ChangeDispatcher()
