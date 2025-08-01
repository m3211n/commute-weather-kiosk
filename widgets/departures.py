from core.ui import Widget, Label
from shared.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(Widget):
    def __init__(self, position):
        super().__init__(
            position=position,
            size=(1160, 368),
            timeout=60)
        self.labelDestination = Label(
            xy=(64, 64),
            fill=Colors.DEFAULT,
            font=Fonts.TITLE
        )
        self.content = [
            self.labelDestination
        ]


class Trains(Departures):
    def __init__(self):
        super().__init__(position=(24, 376))
        self.labelDestination.text = "Stockholm City"


class Busses(Departures):
    def __init__(self):
        super().__init__(position=(24, 768))
        self.labelDestination.text = "Jakobsbergs Station"
        # self.labelDestination.text = "Handen Station"
