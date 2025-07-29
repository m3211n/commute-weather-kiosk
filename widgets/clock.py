from datetime import datetime
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
        self.labelTime.callback = lambda: self._time_str(
            self.labelTime,
            TIME_FORMAT
        )

        self.labelDate = Label(
                xy=(474, 300),
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
        )
        self.labelDate.callback = lambda: self._time_str(
            self.labelDate,
            DATE_FORMAT
        )

        self.content = [self.labelTime, self.labelDate]

    @staticmethod
    def _time_str(label: Label, f):
        new_text = datetime.now().strftime(f)
        if not label.text == new_text:
            label.text = new_text
            return True
        return False
