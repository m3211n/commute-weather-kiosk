from core.ui import ColorWidget, Label
from shared.styles import Colors, Fonts


class Weather(ColorWidget):
    def __init__(self, timeout):
        super().__init__(
            xy=(1208, 24), size=(688, 1112), timeout=timeout
        )
        self.children = [
            Label(
                callback=self._temperature,
                xy=(90, 90),
                font=Fonts.WEATHER_TODAY,
                fill=Colors.DEFAULT,
                anchor="lt"
            ),
            Label(
                callback=self._conditions,
                xy=(90, 210),
                font=Fonts.LABEL_SMALL,
                fill=Colors.SECONDARY,
                anchor="lt"
            )
        ]

    @staticmethod
    def _temperature():
        return "24°C"

    @staticmethod
    def _conditions():
        return "Clear"
