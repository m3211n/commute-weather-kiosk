from core.data_sources import Local
from core.ui import (
    Widget, TextWidget, ImageWidget
)
from core.styles import Fonts, Colors
# import logging


class Info(Widget):
    def __init__(self, interval=1):
        super().__init__(
            position=(0, 1136),
            size=(1920, 64),
            fill=(0, 0, 0, 255),
            interval=interval
            )
        self.children = [
            TextWidget(
                position=(16, 32),
                color=Colors.TITLE,
                font=Fonts.STATUS,
                anchor="lm",
                update_callback=self._host_info,
            ),
            TextWidget(
                position=(1888, 32),
                color=Colors.TITLE,
                font=Fonts.STATUS,
                anchor="rm",
                update_callback=self._hw_stats,
            )
        ]

    def _host_info(self):
        host_info = [
            f"WI-FI SSID: {Local.ssid()}",
            f"IPv4: {Local.hostname('-I')}",
            Local.hostname()
        ]
        return " | ".join(host_info)

    def _hw_stats(self):
        cpu = Local.cpu()
        ram = Local.ram()
        hw_info = [
            f"Available RAM: {ram} MB",
            f"CPU Temp: {cpu[0]:.1f}°C",
            f"CPU Load: {round(cpu[1] * 100, 1)}%"
        ]
        return " | ".join(hw_info)


class Clock(Widget):
    def __init__(self):
        super().__init__(
            update_callback=None,
            position=(24, 24),
            size=(1160, 328),
            fill=Colors.NONE
            )
        self.children = [
            ImageWidget(
                url="./shared/images/clock-bg-night.png",
                update_callback=self._get_image
            ),
            TextWidget(
                update_callback=self._get_time,
                position=(90, 90),
                font=Fonts.CLOCK,
                color=Colors.DEFAULT
            ),
            TextWidget(
                update_callback=self._get_weekday,
                position=(1070, 90),
                font=Fonts.LABEL_SMALL,
                color=Colors.SECONDARY,
                anchor="rt"
            ),
            TextWidget(
                position=(1070, 142),
                font=Fonts.LABEL_SMALL,
                color=Colors.SECONDARY,
                anchor="rt",
                update_callback=self._get_day
            ),
            TextWidget(
                position=(1070, 194),
                font=Fonts.LABEL_LARGE,
                color=Colors.SECONDARY,
                anchor="rt",
                update_callback=self._get_year
            )
        ]

    @staticmethod
    def _get_time():
        return Local.time("%H:%M")

    @staticmethod
    def _get_weekday():
        return Local.time("%A")

    @staticmethod
    def _get_day():
        return Local.time("%B %d")

    @staticmethod
    def _get_year():
        return Local.time("%Y")

    @staticmethod
    def _get_image():
        hours = Local.hours()
        if 4 <= hours < 11:
            return "./shared/images/clock-bg-morning.png"
        elif 11 <= hours < 17:
            return "./shared/images/clock-bg-day.png"
        elif 17 <= hours < 23:
            return "./shared/images/clock-bg-evening.png"
        else:
            return "./shared/images/clock-bg-night.png"
