from widgets.base import Widget, Label
from datetime import datetime
from shared.styles import Fonts, Colors

DATE = "%A, %d, %B, %Y"
TIME = "%H:%M"

time_str = lambda format: datetime.now().strftime(format)

class Clock(Widget):
    def __init__(self, interval=60):
        super().__init__("Clock", interval=interval, position=(8, 8), size=(948, 472))
        self.text_content = {
            "time": Label(
                xy=(474, 236),
                text="--:--",
                fill=Colors.default,
                font=Fonts.clock,
                anchor="mb"
            ),
            "date": Label(
                xy=(474, 252),
                text="Today",
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
            )
        }
    
    async def callback(self):
        self.text_content["time"].text = time_str(TIME)
        self.text_content["date"].text = time_str(DATE)