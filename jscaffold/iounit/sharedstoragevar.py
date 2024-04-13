from .variable import Variable
from ..context import Context
from jscaffold.services.sharedstorage import SharedStorage, shared_storage


class SharedStorageVar(Variable):
    def __init__(self, key, shared_storage: SharedStorage = shared_storage):
        super().__init__()
        self._key = key
        self._shared_storage = shared_storage

    def _get_key(self):
        return self._key

    def _get_id(self):
        return f"SharedStorage:{self.key}"

    def _write(self, value=None, context: Context = None):
        validaed_value = self.validate(value, self.format.defaults)
        self._shared_storage.set(self.key, validaed_value)
        if context is not None and context.log is not None:
            context.log(f"Set {self.key}={value}\n")

    def _read(self, context: Context = None):
        return self._shared_storage.get(self.key)
