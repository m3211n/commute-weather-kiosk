from core.data_sources import Local
from core.ui import ColorWidget, Label, ImageWidget
from shared.styles import Fonts, Colors
import logging


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


class Clock(ImageWidget):

    TIME_FORMAT = "%H:%M"

    def __init__(self):
        daytime_str = Local.daytime()
        super().__init__(
            xy=(24, 24),
            size=(1160, 328),
            img_url=f"./shared/images/clock-bg-{daytime_str}.png",
            timeout=0
        )
        self.current_time_ref = "--:--"
        self.children = [
            Label(
                callback=self._get_time,
                xy=(90, 90),
                font=Fonts.CLOCK,
                anchor="lt"
            ),
            Label(
                callback=self._get_weekday,
                xy=(1070, 90),
                font=Fonts.LABEL_SMALL,
                anchor="rt"
            ),
            Label(
                callback=self._get_day,
                xy=(1070, 142),
                font=Fonts.LABEL_SMALL,
                anchor="rt"
            ),
            Label(
                callback=self._get_year,
                xy=(1070, 194),
                font=Fonts.LABEL_LARGE,
                anchor="rt"
            )
        ]

    def _update_timer(self):
        current_time = self._get_time()
        if self.current_time_ref != current_time:
            debug_msg = " ".join(
                (
                    "Clock updating got triggered:",
                    f"{current_time} != {self.current_time_ref}"
                )
            )
            logging.debug(debug_msg)
            self.current_time_ref = current_time
            return True
        return False

    @staticmethod
    def _get_time():
        return Local.time(Clock.TIME_FORMAT)

    @staticmethod
    def _get_weekday():
        return Local.time("%A")

    @staticmethod
    def _get_day():
        return Local.time("%B %d")

    @staticmethod
    def _get_year():
        return Local.time("%Y")
