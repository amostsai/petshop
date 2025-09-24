import threading
import time
from typing import Any, Optional


class SimpleCache:
    """Thread-safe in-memory cache with optional TTL support."""

    def __init__(self):
        self._store: dict[str, tuple[Optional[float], Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Any:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            expires_at, value = entry
            if expires_at and expires_at <= time.time():
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires_at = time.time() + ttl if ttl else None
        with self._lock:
            self._store[key] = (expires_at, value)

    def invalidate(self, prefix: Optional[str] = None) -> None:
        with self._lock:
            if prefix is None:
                self._store.clear()
                return
            keys_to_delete = [key for key in self._store if key.startswith(prefix)]
            for key in keys_to_delete:
                del self._store[key]


cache = SimpleCache()
