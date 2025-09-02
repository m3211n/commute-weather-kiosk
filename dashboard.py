import updaters
import asyncio

from inspect import isawaitable
from core.ui import Widget, ImageView, Rect, Text
from shared.styles import Colors, TextStyles
from typing import Any, Awaitable, Callable, Dict, Union


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

        self.add_widget(
            name="Info",
            widget=Widget(
                xy=(0, 1136), size=(1920, 64), fill=(0, 0, 0, 255),
                content={
                    "host_info": Text(xy=(16, 32), **TextStyles.status),
                    "sys_info":  Text(xy=(1888, 32), **TextStyles.status_rt)
                }
            ),
            updater=updaters.sys_info,
            int_s=5
        )
        self.add_widget(
            name="Clock",
            widget=Widget(
                xy=(24, 24), size=(1160, 386),
                content={
                    "bg":   ImageView(),
                    "time": Text(xy=(580, 34),  **TextStyles.time),
                    "date": Text(xy=(580, 262), **TextStyles.date)
                }
            ),
            updater=updaters.time_date,
            int_s=1
        )
        self.add_widget(
            name="Weather",
            widget=Widget(
                xy=(1208, 24), size=(688, 1112),
                content={
                    "bg":      ImageView(),
                    "temp":    Text(xy=(64, 34),   **TextStyles.temperature),
                    "icon":    ImageView(498, 90),
                    "desc":    Text(xy=(64, 262),  **TextStyles.weather_cond),
                    "more":    Text(xy=(64, 318),  **TextStyles.details),
                    "icon_sr": Text(xy=(64, 362),  **TextStyles.icon,
                                    value="\uf051"),
                    "sunrise": Text(xy=(128, 372), **TextStyles.details),
                    "icon_ss": Text(xy=(286, 362), **TextStyles.icon,
                                    value="\uf052"),
                    "sunset":  Text(xy=(350, 372), **TextStyles.details),
                    "hours":   Text(xy=(70, 504),  **TextStyles.hours),
                    "icons":   Text(xy=(196, 500), **TextStyles.weather_icons),
                    "temps":   Text(xy=(280, 504), **TextStyles.temps)
                }
            ),
            updater=updaters.weather,
            int_s=900
        )
        self.add_widget(
            name="Departures",
            widget=Widget(
                xy=(24, 434), size=(1160, 702), fill=Colors.panel_bg,
                radius=32,
                content={
                    "title_train":   Text(
                        xy=(64, 58),   **TextStyles.transport_title,
                        value="Pendeltåg mot Nynäshamn"),
                    "train_line":    Text(
                        xy=(64, 117), **TextStyles.line_codes),
                    "train_dest":    Text(
                        xy=(208, 117), **TextStyles.destinations),
                    "train_display": Text(
                        xy=(1096, 117),  **TextStyles.departures),
                    "rect":          Rect(
                        (64, 350, 1096, 352), radius=1,
                        fill=(255, 255, 255, 32)),
                    "title_bus":     Text(
                        xy=(64, 386),  **TextStyles.transport_title,
                        value="Buss mot Jakobsberg C"),
                    "bus_line":      Text(
                        xy=(64, 447), **TextStyles.line_codes),
                    "bus_dest":      Text(
                        xy=(208, 447), **TextStyles.destinations),
                    "bus_display":   Text(
                        xy=(1096, 447),  **TextStyles.departures)
                }
            ),
            updater=updaters.departures,
            int_s=60
        )

    def add_widget(self, name: str, widget: Widget, updater, int_s: int):
        self.widgets[name] = widget

        async def loop():
            while True:
                widget.state = await _call_updater(updater)
                await asyncio.sleep(int_s)

        self.tasks.append(loop())

    async def run(self):
        if len(self.widgets) == 0:
            raise ValueError("Dashboard is empty!")
        await asyncio.gather(*self.tasks)
