from typing import Any


class MockRedis:
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self.local_storage = {}

    def set(self, object_id: str, data: Any):
        self.local_storage[object_id] = data

    def get(self, object_id: str) -> Any:
        return self.local_storage.get(object_id)
