import labels
import updaters
import asyncio

from inspect import iscoroutinefunction as iscoro
from core.ui import Widget, ImageView, Rect
from shared.styles import Colors


class Dashboard:
    def __init__(self):

        self.widgets = {
            "info":         Widget(
                xy=(0, 1136), size=(1920, 64), fill=(0, 0, 0, 255),
                content={
                    "host_info":    labels.status(16, 32, anchor="lm"),
                    "sys_info":     labels.status(1888, 32, anchor="rm")
                }
            ),
            "clock":        Widget(
                xy=(24, 24), size=(1160, 386),
                content={
                    "clock_image":  ImageView(),
                    "time":         labels.time(64, 94),
                    "date":         labels.date(64, 268)
                }
            ),
            "weather":      Widget(
                xy=(1208, 24), size=(688, 1112),
                content={
                    "weather_image": ImageView(),
                    "icon_sr": labels.icon(64, 362, value="\uf051"),
                    "sunrise": labels.regular(128, 370, size=32, anchor="lt"),
                    "icon_ss": labels.icon(286, 362, value="\uf052"),
                    "sunset": labels.regular(350, 370, size=32, anchor="lt"),
                    "temp": labels.temp_now(64, 90),
                    "desc": labels.regular(64, 268, size=40, anchor="lt"),
                    "more": labels.regular(64, 318, size=32, anchor="lt"),
                    "icon": ImageView(498, 90),
                    "hours": labels.regular(70, 504, size=32, spacing=38,
                                            accent=False),
                    "icons": labels.icon(196, 500, spacing=31, align="center"),
                    "temps": labels.regular(280, 504, size=32, spacing=38)
                }
            ),
            "departures":   Widget(
                xy=(24, 434), size=(1160, 702), fill=Colors.PANEL_BG,
                radius=64,
                content={
                    "title_train":      labels.regular(
                        64, 64, size=32, value="Pendeltåg mot Nynäshamn",
                        accent=False, anchor="lt"),
                    "train_display":    labels.departures(64, 117),
                    "train_line":       labels.lines(284, 117),
                    "train_dest":       labels.destinations(420, 117),
                    "rect":             Rect(
                        (64, 350, 1096, 352), radius=1,
                        fill=(255, 255, 255, 32)),
                    "title_bus":        labels.regular(
                        64, 394, size=32, value="Buss mot Jakobsberg C",
                        accent=False, anchor="lt"),
                    "bus_display":      labels.departures(64, 447),
                    "bus_line":         labels.lines(284, 447),
                    "bus_dest":         labels.destinations(420, 447),
                }
            )
        }
        self.updaters = {
            "info":         updaters.sys_info,
            "clock":        updaters.time_date,
            "weather":      updaters.weather,
            "departures":   updaters.departures
        }
        self.tasks = [
            self.get_loop("info", 5),
            self.get_loop("clock", 1),
            self.get_loop("weather", 900),
            self.get_loop("departures", 60)
        ]

    async def run_once(self):
        for key in self.widgets.keys():
            w = self.widgets[key]
            u = self.updaters[key]
            w.state = await u() if iscoro(u) else u()

    def get_loop(self, key: str, int_s: int):
        widget = self.widgets[key]
        widget._name = key
        upd = self.updaters[key]

        async def loop():
            while True:
                widget.state = await upd() if iscoro(upd) else upd()
                await asyncio.sleep(int_s)

        return loop()

    async def run_forever(self):
        await asyncio.gather(*self.tasks)
