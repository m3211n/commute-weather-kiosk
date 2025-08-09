from core.data_sources import Local
from core.elements import Widget, TextLabel, Img
from shared.styles import Fonts, Colors
# import logging


class Info(Widget):
    def __init__(self):
        super().__init__(xy=(0, 1136), size=(1920, 64), fill=(0, 0, 0, 255))
        self.hostinfo = TextLabel(
            xy=(16, 32), color=Colors.TITLE, font=Fonts.STATUS, anchor="lm",
            callback=self._get_hostinfo
        )
        self.sysinfo = TextLabel(
            xy=(1888, 32), color=Colors.TITLE, font=Fonts.STATUS, anchor="rm",
            callback=self._get_sysinfo
        )
        self.children = [
            self.hostinfo,
            self.sysinfo
        ]

    def _get_hostinfo(self):
        host_info = [
            f"WI-FI SSID: {Local.ssid()}",
            f"IPv4: {Local.hostname('-I')}",
            Local.hostname()
        ]
        return " | ".join(host_info)

    def _get_sysinfo(self):
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
        super().__init__(xy=(24, 24), size=(1160, 328))
        self.bg = Img(callback=self._get_time_image)
        self.time = TextLabel(
            xy=(90, 90), font=Fonts.CLOCK, color=Colors.DEFAULT,
            callback=lambda: Local.time("%H:%M")
        )
        self.date_0 = TextLabel(
            xy=(1070, 90), font=Fonts.LABEL_SMALL, color=Colors.SECONDARY,
            anchor="rt",
            callback=lambda: Local.time("%A")
        )
        self.date_1 = TextLabel(
            xy=(1070, 142), font=Fonts.LABEL_SMALL, color=Colors.SECONDARY,
            anchor="rt",
            callback=lambda: Local.time("%B %d")
        )
        self.date_2 = TextLabel(
            xy=(1070, 194), font=Fonts.LABEL_LARGE, color=Colors.SECONDARY,
            anchor="rt",
            callback=lambda: Local.time("%Y")
        )
        self.children = [
            self.bg,
            self.time,
            self.date_0,
            self.date_1,
            self.date_2
        ]

    async def _get_time_image(self):
        daytime = Local.daytime()
        return f"./shared/images/clock/{daytime}.png"
