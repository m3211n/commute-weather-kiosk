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
                children={
                    "host_info":    labels.status(16, 32),
                    "sys_info":     labels.status(1888, 32, "rm")
                }
            ),
            "clock": Widget(
                xy=(24, 24), size=(1160, 328),
                children={
                    "clock_image":  Img(),
                    "time":         labels.clock(90, 90),
                    "date_0":       labels.small(1070, 90),
                    "date_1":       labels.small(1070, 142),
                    "date_2":       labels.large(1070, 194)
                }
            ),
            "weather": Widget(
                xy=(1208, 24), size=(688, 1112),
                children={
                    "weather_image": Img(),
                    "temp":         labels.temp_now(90, 90),
                    "icon":         Img(470, 100),
                    "feels_like":   labels.small(90, 278, "lt"),
                    "fill":         Rect(xy=(50, 400, 638, 1040),
                                         fill=(0, 0, 0, 80), radius=48),
                    "hours":        labels.small(90, 440, "lt"),
                    "values":       labels.small(228, 440, "lt")
                }
            ),
            "trains": Widget(
                xy=(24, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                children={
                    "title":        labels.title(40, 40),
                    "direction":    labels.large(40, 84),
                    "destinations": labels.destination(40, 244),
                    "departures":   labels.departutes(40, 244)
                }
            ),
            "buses": Widget(
                xy=(616, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                children={
                    "title":        labels.title(40, 40),
                    "direction":    labels.large(40, 84),
                    "destinations": labels.destination(40, 244),
                    "departures":   labels.departutes(40, 244)
                }
            )
        }
        self.updaters = {
            "info": updaters.sys_info,
            "clock": updaters.time_date,
            "weather": updaters.weather,
            "trains": updaters.trains,
            "buses": updaters.buses
        }
        self.intervals = {
            "info": 5,
            "clock": 1,
            "weather": 900,
            "trains": 60,
            "buses": 60
        }

    def get_loop(self, key: str, interval_s: int):
        widget = self.widgets[key]
        widget._name = key
        updater = self.updaters[key]

        async def loop():
            while True:
                if iscoro(updater):
                    widget.state = await updater()
                else:
                    widget.state = updater()
                await asyncio.sleep(interval_s)

        return loop()

    async def run_forever(self):
        tasks = [
            self.get_loop(key, self.intervals[key])
            for key in self.widgets
        ]
        await asyncio.gather(*tasks)
