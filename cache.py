import time
from typing import Any, Optional, Dict


class Cache:
    def __init__(self, ttl: int = 90):
        self.ttl = ttl
        self._store: Dict[str, Any] = {}
        self._time: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        if time.time() - self._time[key] > self.ttl:
            self.delete(key)
            return None
        return self._store[key]

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._time[key] = time.time()

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
        self._time.pop(key, None)

    def clear(self) -> None:
        self._store.clear()
        self._time.clear()