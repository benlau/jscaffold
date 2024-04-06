class SharedStorage:
    """
    A key-value based shared storage between Jupyter cells
    """

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def remove(self, key):
        if key in self.data:
            del self.data[key]


shared_storage = SharedStorage()
