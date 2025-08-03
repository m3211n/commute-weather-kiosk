from core.ui import Widget, TextWidget, ColorFill
from core.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(Widget):
    def __init__(self, position):
        super().__init__(
            position=position,
            size=(1160, 368),
            interval=1)
        self.children = [
            ColorFill(self),
            TextWidget(
                update_callback=self._title,
                position=(32, 32),
                color=Colors.TITLE,
                font=Fonts.LABEL_SMALL
            )
        ]

    @staticmethod
    def _title():
        return "Default Destination"


class Trains(Departures):
    def __init__(self):
        super().__init__(position=(24, 376))

    @staticmethod
    def _title():
        return "Train Destination"


class Busses(Departures):
    def __init__(self):
        super().__init__(position=(24, 768))

    @staticmethod
    def _title():
        return "Bus Destination"
