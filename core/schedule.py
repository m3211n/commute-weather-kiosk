import asyncio
import logging

from typing import Callable, Awaitable, Dict, Any
from core.store import Store


def every(interval_s: int, func: Callable[[], Dict[str, Any]], store: Store):
    async def loop():
        while True:
            try:
                data = func()
                if isinstance(data, dict):
                    await store.set_many(data)
            except Exception as e:
                logging.exception(f"[local updater] {e}")
            await asyncio.sleep(interval_s)
    return loop()


def every_async(
        interval_s: int, coro: Callable[[], Awaitable[Dict[str, Any]]],
        store: Store):
    async def loop():
        while True:
            try:
                data = await coro()
                if isinstance(data, dict):
                    await store.set_many(data)
            except Exception as e:
                print(f"[async updater] {e}")
            await asyncio.sleep(interval_s)
    return loop()
