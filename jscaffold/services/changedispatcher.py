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
        payload_type = (
            payload["type"] if payload is not None and "type" in payload else None
        )

        debounce_key = f"{key}:{payload_type}" if payload_type is not None else key

        self.debouncer(debounce_key, self._invoke_listeners, key, payload)

    def _invoke_listeners(self, key, payload):
        pending_remove_list = []
        for listener in self.listeners:
            try:
                listener(key, payload)
            except Exception:
                pending_remove_list.append(listener)

        for listener in pending_remove_list:
            self.listeners.remove(listener)


class Listener:
    def __init__(self, type, callback):
        self.type = type
        self.callback = callback

    def __call__(self, type, payload):
        if self.type == type:
            self.callback(payload)


change_dispatcher = ChangeDispatcher()
