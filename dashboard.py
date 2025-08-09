from core.styles import Fonts, Colors
from core.elements import Widget, TextLabel, Icon
from typing import List


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200


class Clock(Widget):
    def __init__(self, update_interval=60):
        super().__init__(
            xy=(24, 24),
            size=(1160, 328),
            bg_img="./shared/images/clock/morning.png"
        )
        self.time_label = TextLabel(
            xy=(90, 90), color=Colors.DEFAULT, font=Fonts.CLOCK
        )
        self.day = TextLabel(
            xy=(90, 90), color=Colors.DEFAULT, font=Fonts.LABEL_SMALL,
            anchor="rt"
        )
        self.month_date = TextLabel(
            xy=(142, 90), color=Colors.DEFAULT, font=Fonts.LABEL_SMALL,
            anchor="rt"
        )
        self.year = TextLabel(
            xy=(194, 90), color=Colors.DEFAULT, font=Fonts.LABEL_LARGE,
            anchor="rt"
        )

    def set_text(self, time_data):
        self.time_label.set_text("12:34")
        self.day.set_text("måndag")
        self.month_date.set_text("september, 31")
        self.year.set_text("2025")


class Dashboard(Widget):
    def __init__(self, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        super().__init__(xy=(0, 0), size=size)
        self.widgets: List[Widget] = {
            "clock": Clock(60),
            "train": Widget(),
            "bus": Widget(),
            "weather": Widget()
        }

    async def update_widgets(self):
        self.widgets["clock"].update()