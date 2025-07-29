from widgets.data_sources import get_time
from widgets.core import Widget, Label
from shared.styles import Colors, Fonts

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%A, %B %d, %Y"


class Clock(Widget):
    def __init__(self):
        super().__init__(position=(8, 8), size=(948, 472))

        self.labelTime = Label(
                xy=(474, 268),
                fill=Colors.default,
                font=Fonts.clock,
                anchor="mb"
        )
        self.labelTime.update = lambda: self._time_str(
            self.labelTime,
            TIME_FORMAT
        )

        self.labelDate = Label(
                xy=(474, 300),
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
        )
        self.labelDate.update = lambda: self._time_str(
            self.labelDate,
            DATE_FORMAT
        )

        self.content = [self.labelTime, self.labelDate]

    @staticmethod
    def _time_str(label: Label, f):
        current_time = get_time(f)
        if not label.text == current_time:
            label.text = current_time
            return True
        return False
