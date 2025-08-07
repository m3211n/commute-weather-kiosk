from core.widget import Widget, TextWidget, ColorFill
from core.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(Widget):
    def __init__(self, position, interval):
        super().__init__(
            position=position,
            size=(1160, 368),
            interval=interval)
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
    def __init__(self, interval):
        super().__init__(position=(24, 376), interval=interval)

    @staticmethod
    def _title():
        return "Train Destination"


class Busses(Departures):
    def __init__(self, interval):
        super().__init__(position=(24, 768), interval=interval)

    @staticmethod
    def _title():
        return "Bus Destination"
