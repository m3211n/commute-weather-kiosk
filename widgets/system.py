from widgets.data_sources import Local
from core.ui import Widget, Label
from shared.styles import Fonts, Colors


class Info(Widget):
    def __init__(self, timeout=5):
        super().__init__(
            position=(8, 1144), size=(1904, 48), bgcolor=Colors.NONE
            )
        self.timeout = timeout
        self.labelLeft = Label(
            xy=(16, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="lm"
        )
        self.labelRight = Label(
            xy=(1888, 24),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="rm"
        )

    async def update_content(self) -> bool:
        if self._update_timeout():
            host_info = [
                f"WI-FI SSID: {Local.ssid()}",
                f"IPv4: {Local.hostname('-I')}",
                Local.hostname()
            ]
            self.labelLeft.text = " | ".join(host_info)
            cpu = Local.cpu()
            hw_info = [
                f"CPU Temp: {cpu[0]:.1f}°C",
                f"CPU Load: {round(cpu[1] * 100, 1)}%"
            ]
            self.labelRight.text = " | ".join(hw_info)
            return True
        return False

    async def render(self):
        self._clear()
        await self.labelLeft.render_at(self.image)
        await self.labelRight.render_at(self.image)


class Clock(Widget):

    TIME_FORMAT = "%H:%M"
    DATE_FORMAT = "%A-%B %d-%Y"

    def __init__(self):
        super().__init__(
            position=(24, 24),
            radius=64,
            size=(1160, 328)
            )
        self.labelTime = Label(
            xy=(64, 90),
            font=Fonts.CLOCK,
            anchor="lt"

        )
        self.labelWeekday = Label(
            xy=(1096, 90),
            fill=Colors.SECONDARY,
            font=Fonts.TITLE,
            anchor="rt"
        )
        self.labelDate = Label(
            xy=(1096, 134),
            fill=Colors.SECONDARY,
            font=Fonts.TITLE,
            anchor="rt"
        )
        self.labelYear = Label(
            xy=(1096, 178),
            fill=Colors.SECONDARY,
            font=Fonts.VALUE,
            anchor="rt"
        )

    async def update_content(self):
        current_time = Local.time(Clock.TIME_FORMAT)
        weekday, date, year = Local.time(Clock.DATE_FORMAT).split("-")
        if self.labelTime.text != current_time:
            self.labelTime.text = current_time
            self.labelWeekday.text = weekday
            self.labelDate.text = date
            self.labelYear.text = year
            return True
        return False

    async def render(self):
        self._clear()
        await self.labelTime.render_at(self.image)
        await self.labelWeekday.render_at(self.image)
        await self.labelDate.render_at(self.image)
        await self.labelYear.render_at(self.image)
