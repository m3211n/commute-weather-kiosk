import labels
import updaters
import asyncio

from inspect import iscoroutinefunction as iscoro
from core.ui import Widget, Img, Rect
from shared.styles import Colors


class Dashboard:
    def __init__(self):
        self.widgets = {
            "info": Widget(
                xy=(0, 1136), size=(1920, 64), fill=(0, 0, 0, 255),
                content={
                    "host_info":    labels.status(16, 32),
                    "sys_info":     labels.status(1888, 32, "rm")
                }
            ),
            "clock": Widget(
                xy=(24, 24), size=(1160, 328),
                content={
                    "clock_image":  Img(),
                    "time":         labels.clock(90, 90),
                    "date_0":       labels.small(1070, 90),
                    "date_1":       labels.small(1070, 142),
                    "date_2":       labels.large(1070, 194)
                }
            ),
            "weather": Widget(
                xy=(1208, 24), size=(688, 1112),
                content={
                    "weather_image": Img(),
                    "temp":         labels.temp_now(90, 90),
                    "icon":         Img(470, 74),
                    "feels_like":   labels.small(90, 210, "lt"),
                    "min_max":      labels.x_small(90, 270, "lt"),
                    "fill":         Rect(xy=(50, 400, 638, 1040),
                                         fill=(0, 0, 0, 63), radius=48),
                    "hours":        labels.small(90, 440, "lt"),
                    "values":       labels.small(228, 440, "lt")
                }
            ),
            "trains": Widget(
                xy=(24, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                content={
                    "title":        labels.title(40, 40),
                    "direction":    labels.large(40, 84),
                    "destinations": labels.destination(40, 244),
                    "departures":   labels.departutes(40, 244)
                }
            ),
            "buses": Widget(
                xy=(616, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                content={
                    "title":        labels.title(40, 40),
                    "direction":    labels.large(40, 84),
                    "destinations": labels.destination(40, 244),
                    "departures":   labels.departutes(40, 244)
                }
            )
        }
        self.tasks = [
            self.get_loop("info", updaters.sys_info, 5),
            self.get_loop("clock", updaters.time_date, 1),
            self.get_loop("weather", updaters.weather, 900),
            self.get_loop("trains", updaters.trains, 60),
            self.get_loop("buses", updaters.buses, 60)
        ]

    def get_loop(self, key: str, upd, int_s: int):
        widget = self.widgets[key]
        widget._name = key

        async def loop():
            while True:
                widget.state = await upd() if iscoro(upd) else upd()
                await asyncio.sleep(int_s)

        return loop()

    async def run_forever(self):
        await asyncio.gather(*self.tasks)
