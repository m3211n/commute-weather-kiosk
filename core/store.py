import asyncio
from collections import defaultdict
from typing import Any, Dict


class Store:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._subs = defaultdict(list)  # key -> list[asyncio.Queue]

    async def get(self, key: str, default=None):
        return self._data.get(key, default)

    async def set(self, key: str, value: Any):
        async with self._lock:
            old = self._data.get(key, object())
            if old != value:
                self._data[key] = value
                for q in self._subs[key]:
                    q.put_nowait(value)  # non-blocking notify

    async def set_many(self, items: Dict[str, Any]):
        async with self._lock:
            changed = []
            for k, v in items.items():
                if self._data.get(k, object()) != v:
                    self._data[k] = v
                    changed.append(k)
        for k in changed:
            for q in self._subs[k]:
                q.put_nowait(self._data[k])

    def subscribe(self, key: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=1)
        self._subs[key].append(q)
        return q
