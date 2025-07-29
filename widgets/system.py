from data_sources import Local
from widgets.core import Widget, Label
from shared.styles import Fonts, Colors


class Info(Widget):
    def __init__(self):
        super().__init__(position=(8, 1128), size=(1904, 64))
        self.labelLeft = Label(
            xy=(16, 32),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="lm"
        )
        self.labelRight = Label(
            xy=(1888, 32),
            fill=Colors.TITLE,
            font=Fonts.STATUS,
            anchor="rm"
        )

    async def update_content(self) -> bool:
        self.labelLeft.text = f"SSID: {Local.ssid()} ({Local.ip_address()})"
        cpu = Local.cpu()
        temp = cpu[0]
        load = f"{round((cpu[1] + cpu[2] + cpu[3]) * 100 / 3, 1)}%"
        self.labelRight.text = f"CPU: {temp} (Avg.load: {load})"
        return True

    async def render(self):
        self._clear()
        await self.label.render_at(self.image)


class Clock(Widget):

    TIME_FORMAT = "%H:%M"
    DATE_FORMAT = "%A, %B %d, %Y"

    def __init__(self):
        super().__init__(position=(8, 8), size=(948, 548))
        self.labelTime = Label(
            xy=(474, 314),
            font=Fonts.CLOCK,
            anchor="mb"
        )
        self.labelDate = Label(
            xy=(474, 336),
            fill=Colors.SECONDARY,
            font=Fonts.TITLE,
            anchor="mt"
        )

    async def update_content(self):
        current_time = Local.time(Clock.TIME_FORMAT)
        if self.labelTime.text != current_time:
            self.labelTime.text = current_time
            self.labelDate.text = Local.time(Clock.DATE_FORMAT)
            return True
        return False

    async def render(self):
        self._clear()
        await self.labelTime.render_at(self.image)
        await self.labelDate.render_at(self.image)
