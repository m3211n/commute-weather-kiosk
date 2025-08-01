from core.ui import ColorWidget, Label
from shared.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(ColorWidget):
    def __init__(self, position):
        super().__init__(
            xy=position,
            size=(1160, 368),
            timeout=60)
        self.children = [
            Label(
                callback=self._title,
                xy=(32, 32),
                fill=Colors.TITLE,
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
