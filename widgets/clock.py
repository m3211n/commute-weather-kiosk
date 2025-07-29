from widgets.base import Widget, Label
from datetime import datetime
from shared.styles import Fonts, Colors

DATE = "%A, %d, %B, %Y"
TIME = "%H:%M"

time_str = lambda format: datetime.now().strftime(format)

class Clock(Widget):
    def __init__(self, interval=60):
        super().__init__("Clock", (8, 8), (948, 472))
        self.time = Label("--:--", font=Fonts.clock, anchor="mb", fill=Colors.default)
        self.date = Label("Today", font=Fonts.title, anchor="mt", position=(0, 16), fill=Colors.title)
        self._interval = interval

    async def callback(self):
        await self.time.update(time_str(TIME))
        await self.date.update(time_str(DATE))