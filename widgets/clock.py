from widgets.base import Widget, Label
from datetime import datetime
from shared.styles import Fonts, Colors

DATE = "%A, %B %d, , %Y"
TIME = "%H:%M"
MIN = "%-M"

time_str = lambda format: datetime.now().strftime(format)

class Clock(Widget):
    def __init__(self, interval=1):
        super().__init__("Clock", interval=interval, position=(8, 8), size=(948, 472))
        self._current_minute = -1
        self._in_sync = lambda: self._current_minute == datetime.now().minute
        self.text_content = {
            "time": Label(
                xy=(474, 268),
                text=time_str(TIME),
                fill=Colors.default,
                font=Fonts.clock,
                anchor="mb"
            ),
            "date": Label(
                xy=(474, 300),
                text=time_str(DATE),
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
            )
        }
    
    async def update_content(self):
        if not self._in_sync:
            self._current_minute = datetime.now().minute
            self.text_content["time"].text = time_str(TIME)
            self.text_content["date"].text = time_str(DATE)
            return True
        else:
            return False