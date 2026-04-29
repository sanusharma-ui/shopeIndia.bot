import time
from config import settings


class TTLCache:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 1000):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.store: dict[str, tuple[float, object]] = {}

    def get(self, key: str):
        item = self.store.get(key)

        if not item:
            return None

        created_at, value = item

        if time.time() - created_at > self.ttl_seconds:
            self.store.pop(key, None)
            return None

        return value

    def set(self, key: str, value):
        if len(self.store) >= self.max_size:
            oldest_key = min(self.store, key=lambda k: self.store[k][0])
            self.store.pop(oldest_key, None)

        self.store[key] = (time.time(), value)


response_cache = TTLCache(
    ttl_seconds=settings.CACHE_TTL_SECONDS,
    max_size=3000
)