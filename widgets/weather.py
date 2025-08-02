from core.ui import Widget, ImageWidget, TextWidget
from core.styles import Colors, Fonts
from core.data_sources import WeatherData


class Weather(Widget):
    def __init__(self, interval=900):
        super().__init__(
            position=(1208, 24),
            size=(688, 1112),
            fill=Colors.NONE,
            interval=interval
            )
        self.children = [
            ImageWidget(
                url="./shared/images/weather-clear-night.png"
            ),
            TextWidget(
                update_callback=self._temperature,
                position=(90, 90),
                font=Fonts.WEATHER_TODAY,
                color=Colors.DEFAULT
            ),
            TextWidget(
                update_callback=self._conditions,
                position=(90, 210),
                font=Fonts.LABEL_SMALL,
                color=Colors.SECONDARY
            )
        ]

    @staticmethod
    def _temperature():
        temp = WeatherData.get_current()[0]
        return f"{temp}°C"

    @staticmethod
    def _conditions():
        cond = WeatherData.get_current()[1]
        return cond
