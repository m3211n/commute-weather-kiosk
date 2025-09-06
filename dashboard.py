import asyncio
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Dict, Union

from core.ui import Widget
from layout import WIDGETS


Updater = Callable[[], Union[Dict[str, Any], Awaitable[Dict[str, Any]]]]


async def _call_updater(updater: Updater) -> Dict[str, Any]:
    try:
        res = updater()
        return await res if isawaitable(res) else res
    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise e


class Dashboard:
    def __init__(self):
        self.tasks = []
        self.widgets: Dict[str, Widget] = {}
        for w in WIDGETS:
            self.add_widget(**w)

    def add_widget(self, name: str, widget: Widget, updater: Updater, int_s: int):
        self.widgets[name] = widget

        async def loop():
            while True:
                try:
                    widget.state = await _call_updater(updater)
                except Exception as e:
                    print(f"Error updating widget {name}: {e}")
                await asyncio.sleep(int_s)

        self.tasks.append(loop())

    async def run(self):
        if len(self.widgets) == 0:
            raise ValueError("Dashboard is empty!")
        await asyncio.gather(*self.tasks)
