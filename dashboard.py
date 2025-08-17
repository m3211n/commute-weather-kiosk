import labels
import updaters
import asyncio

from inspect import iscoroutinefunction as iscoro
from core.ui import Widget, Img
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
                    "time":         labels.time(580, 64),
                    "date":         labels.date(580, 236)
                }
            ),
            "weather": Widget(
                xy=(1208, 24), size=(688, 1112),
                content={
                    "weather_image": Img(),
                    "icon_sr":      labels.static_icon(
                        64, 342, value="\uf051"),
                    "sunrise":      labels.h3(
                        128, 350, accent=True, anchor="lt"),
                    "icon_ss":      labels.static_icon(
                        286, 342, value="\uf052"),
                    "sunset":      labels.h3(
                        350, 350, accent=True, anchor="lt"),
                    "temp":         labels.temp_now(64, 64, accent=True),
                    "desc":         labels.feels_like(
                        64, 240, "lt", accent=True),
                    "more": labels.h4(64, 292, "lt", accent=True),
                    "icon":         Img(498, 64),
                    "hours":        labels.h3_block(
                        70, 480, spacing=42),
                    "icons":        labels.icons_block(
                        196, 476, accent=True, spacing=35, align="center"),
                    "temps":        labels.h3_block(
                        276, 480, accent=True, spacing=42)
                }
            ),
            "trains": Widget(
                xy=(24, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                content={
                    "title":        labels.feels_like(40, 40),
                    "direction":    labels.d3(40, 84),
                    "departures":   labels.d2(40, 244)
                }
            ),
            "buses": Widget(
                xy=(616, 376), size=(568, 468), fill=Colors.PANEL_BG,
                radius=24,
                content={
                    "title":        labels.feels_like(40, 40),
                    "direction":    labels.d3(40, 84),
                    "departures":   labels.d2(40, 244)
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
