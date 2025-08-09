from core.data_sources import Local
from core.elements import Widget, TextLabel
from core.styles import Fonts, Colors
# import logging


class Info(Widget):
    def __init__(self):
        super().__init__(
            xy=(0, 1136),
            size=(1920, 64),
            fill=(0, 0, 0, 0)
            )
        self.hostinfo = TextLabel(
            xy=(16, 32),
            color=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="lm"
        )
        self.sysinfo = TextLabel(
            xy=(1888, 32),
            color=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="rm"
        )
        self.children = [
            self.hostinfo,
            self.sysinfo
        ]

    async def update(self):
        hostinfo_dirty = self.hostinfo.set_text(self._get_hostinfo())
        sysinfo_dirty = self.sysinfo.set_text(self._get_sysinfo())
        if any((hostinfo_dirty, sysinfo_dirty)):
            await self.render()
            return True
        return False

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
        self.bg_url = "./shared/images/clock/night.png"
        super().__init__(
            xy=(24, 24),
            size=(1160, 328),
            bg_url=self.bg_url
            )
        self.time = TextLabel(
            xy=(90, 90),
            font=Fonts.CLOCK,
            color=Colors.DEFAULT
        )
        self.date_0 = TextLabel(
            xy=(1070, 90),
            font=Fonts.LABEL_SMALL,
            color=Colors.SECONDARY,
            anchor="rt"
        )
        self.date_1 = TextLabel(
            xy=(1070, 142),
            font=Fonts.LABEL_SMALL,
            color=Colors.SECONDARY,
            anchor="rt"
        )
        self.date_2 = TextLabel(
            xy=(1070, 194),
            font=Fonts.LABEL_LARGE,
            color=Colors.SECONDARY,
            anchor="rt"
        )
        self.children = [
            self.time,
            self.date_0,
            self.date_1,
            self.date_2
        ]

    async def update(self):
        time = self.time.set_text(Local.time("%H:%M"))
        date_0 = self.date_0.set_text(Local.time("%A"))
        date_1 = self.date_1.set_text(Local.time("%B %d"))
        date_2 = self.date_2.set_text(Local.time("%Y"))
        # Update image if needed
        s = f"./shared/images/clock/{Local.daytime()}.png"
        bg_url = (not self.bg_url == s)
        if bg_url:
            self.bg_url = s
            self.bg = self._get_image(self.bg_url)
        if any((time, date_0, date_1, date_2, bg_url)):
            await self.render()
            return True
        return False
