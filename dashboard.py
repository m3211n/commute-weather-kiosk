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
                xy=(24, 24), size=(1160, 386),
                content={
                    "clock_image":  Img(),
                    "time":         labels.time(580, 90),
                    "date":         labels.date(580, 268)
                }
            ),
            "weather": Widget(
                xy=(1208, 24), size=(688, 1112),
                content={
                    "weather_image": Img(),
                    "icon_sr":      labels.static_icon(
                        64, 362, value="\uf051"),
                    "sunrise":      labels.h3(
                        128, 370, anchor="lt"),
                    "icon_ss":      labels.static_icon(
                        286, 362, value="\uf052"),
                    "sunset":      labels.h3(
                        350, 370, anchor="lt"),
                    "temp":         labels.temp_now(64, 90),
                    "desc":         labels.label_40(64, 268, "lt"),
                    "more": labels.h4(64, 318, "lt"),
                    "icon":         Img(498, 90),
                    "hours":        labels.h3_block(
                        70, 504, spacing=38, accent=False),
                    "icons":        labels.icons_block(
                        196, 500, spacing=31, align="center"),
                    "temps":        labels.h3_block(
                        280, 504, spacing=38)
                }
            ),
            "departures": Widget(
                xy=(24, 434), size=(1160, 702), fill=Colors.PANEL_BG,
                radius=64,
                content={
                    "title_train":      labels.h3(
                        64, 64, static_value="Pendeltåg mot Nynäshamn",
                        accent=False, anchor="lt"),
                    "train_display":    labels.departure_block(
                        64, 117, spacing=16),
                    "train_line":       labels.line_block(
                        284, 117, spacing=16),
                    "train_dest":       labels.dest_block(
                        420, 117, spacing=16),
                    "rect":         Rect(
                        (64, 350, 1096, 352), radius=1,
                        fill=(255, 255, 255, 32)),
                    "title_bus":      labels.h3(
                        64, 394, static_value="Buss mot Jakobsberg C",
                        accent=False, anchor="lt"),
                    "bus_display":    labels.departure_block(
                        64, 447, spacing=16),
                    "bus_line":       labels.line_block(
                        284, 447, spacing=16),
                    "bus_dest":       labels.dest_block(
                        420, 447, spacing=16),
                }
            )
        }
        self.tasks = [
            self.get_loop("info", updaters.sys_info, 5),
            self.get_loop("clock", updaters.time_date, 1),
            self.get_loop("weather", updaters.weather, 900),
            self.get_loop("departures", updaters.departures, 60)
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
