from core.data_sources import Local
from core.ui import (
    ColorWidget, Label, Widget, TextWidget, ImageWidget, DrawGroup
)
from core.styles import Fonts, Colors
# import logging


class Info(ColorWidget):
    def __init__(self, timeout=1):
        super().__init__(
            xy=(8, 1144), size=(1904, 48), fill=Colors.NONE, timeout=timeout
            )
        self.labelLeft = Label(
            callback=self._host_info,
            xy=(16, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="lm"
        )
        self.labelRight = Label(
            callback=self._hw_stats,
            xy=(1888, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="rm"
        )
        self.children = [
            self.labelLeft,
            self.labelRight
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
        hw_info = [
            f"CPU Temp: {cpu[0]:.1f}°C",
            f"CPU Load: {round(cpu[1] * 100, 1)}%"
        ]
        return " | ".join(hw_info)


class TestClock(Widget):
    def __init__(self):
        super().__init__(
            position=(24, 24),
            size=(1160, 328),
            fill=Colors.NONE
            )
        self.children = [
            ImageWidget(
                url="./shared/images/clock-bg-night.png"
            ),
            TextWidget(
                position=(90, 90),
                font=Fonts.CLOCK,
                color=Colors.DEFAULT,
                update_callback=self._get_time
            ),
            DrawGroup(
                position=(702, 90),
                size=(368, 148),
                children=[
                    TextWidget(
                        position=(368, 0),
                        font=Fonts.LABEL_SMALL,
                        color=Colors.SECONDARY,
                        anchor="rt",
                        update_callback=self._get_weekday
                    ),
                    TextWidget(
                        position=(368, 52),
                        font=Fonts.LABEL_SMALL,
                        color=Colors.SECONDARY,
                        anchor="rt",
                        update_callback=self._get_day
                    ),
                    TextWidget(
                        position=(368, 104),
                        font=Fonts.LABEL_LARGE,
                        color=Colors.SECONDARY,
                        anchor="rt",
                        update_callback=self._get_year
                    )
                ]
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
