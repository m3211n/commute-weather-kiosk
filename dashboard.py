import asyncio
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Dict, Union

from core.ui import Widget

Updater = Callable[[], Union[Dict[str, Any], Awaitable[Dict[str, Any]]]]


class Dashboard:
    def __init__(self):
        self._tasks = []
        self.widgets: Dict[str, Widget] = {}

    def add_widget(
            self,
            name: str,
            widget: Widget,
            updater: Updater,
            int_s: int):

        async def call(updater: Updater) -> Dict[str, Any]:
            try:
                res = updater()
                return await res if isawaitable(res) else res
            except asyncio.CancelledError:
                raise
            except Exception as e:
                raise e

        async def loop():
            while True:
                try:
                    widget.state = await call(updater)
                    if widget.dirty:
                        widget.update()
                except Exception as e:
                    print(f"Error updating widget {name}: {e}")
                await asyncio.sleep(int_s)

        self.widgets[name] = widget
        # Create the task immediately and store it
        task = asyncio.create_task(loop())
        self._tasks.append(task)

    async def run(self):
        if len(self.widgets) == 0:
            raise RuntimeError("Dashboard is empty!")
        try:
            await asyncio.gather(*self._tasks)
        except KeyboardInterrupt:
            for task in self._tasks:
                task.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            raise

    def get_dirty_widgets(self):
        for name, widget in self.widgets.items():
            if widget.dirty:
                widget.dirty = False
                yield (name, widget)

    def debug(self, path="__preview/output.png", format="PNG"):
        from core.ui import Image
        from defaults import SCREEN_WIDTH, SCREEN_HEIGHT

        image = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT))
        for widget in self.widgets.values():
            image.paste(
                im=widget._canvas(),
                box=tuple(widget.xy),
                mask=widget._canvas().split()[3]
            )
        image.save(fp=path, format=format)
