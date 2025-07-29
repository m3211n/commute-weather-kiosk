from widgets.base import Widget, Label
from datetime import datetime
from shared.styles import Fonts, Colors

DATE = "%A, %d, %B, %Y"
TIME = "%H:%M"

time_str = lambda format: datetime.now().strftime(format)

class Clock(Widget):
    def __init__(self, interval=60):
        super().__init__("Clock", interval=interval, position=(8, 8), size=(948, 472))
        self.content = {
            "time": Label("--:--", font=Fonts.clock, anchor="mb", position=(474, 236), fill=Colors.default),
            "date": Label("Today", font=Fonts.title, anchor="mt", position=(474, 252), fill=Colors.title)
        }
    
    async def callback(self):
        await self.content["time"].update(time_str(TIME))
        await self.content["date"].update(time_str(DATE))