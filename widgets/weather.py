from core.ui import Widget, Label
from shared.styles import Colors, Fonts


class Weather(Widget):
    def __init__(self, timeout=900):
        super().__init__(position=(1208, 24), size=(688, 1112))
        self.timeout = timeout
        self.content = [
            Label(
                update_callback=self._temperature,
                xy=(90, 90),
                font=Fonts.WEATHER_TODAY,
                fill=Colors.DEFAULT,
                anchor="lt"
            ),
            Label(
                update_callback=self._conditions,
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
