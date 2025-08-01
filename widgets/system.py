from core.data_sources import Local
from core.ui import Widget, Label
from shared.styles import Fonts, Colors


class Info(Widget):
    def __init__(self, timeout=5):
        super().__init__(
            position=(8, 1144), size=(1904, 48), bgcolor=Colors.NONE
            )
        self.timeout = timeout
        self.labelLeft = Label(
            update_callback=self._host_info,
            xy=(16, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="lm"
        )
        self.labelRight = Label(
            update_callback=self._hw_stats,
            xy=(1888, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="rm"
        )
        self.content = [
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


class Clock(Widget):

    TIME_FORMAT = "%H:%M"
    DATE_FORMAT = "%A-%B %d-%Y"

    def __init__(self):
        super().__init__(
            position=(24, 24),
            size=(1160, 328)
            )
        self.current_time_ref = "--:--"
        self.content = [
            Label(
                update_callback=self._get_time,
                xy=(90, 90),
                font=Fonts.CLOCK,
                anchor="lt"
            ),
            Label(
                update_callback=self._get_weekday,
                xy=(1070, 90),
                fill=Colors.SECONDARY,
                font=Fonts.LABEL_SMALL,
                anchor="rt"
            ),
            Label(
                update_callback=self._get_day,
                xy=(1070, 142),
                fill=Colors.SECONDARY,
                font=Fonts.LABEL_SMALL,
                anchor="rt"
            ),
            Label(
                update_callback=self._get_year,
                xy=(1070, 194),
                fill=Colors.DEFAULT,
                font=Fonts.LABEL_LARGE,
                anchor="rt"
            )
        ]

    def _update_timeout(self):
        current_time = self._get_time()
        if self.current_time_ref != current_time:
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
