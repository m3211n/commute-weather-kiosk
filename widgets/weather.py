from core.ui import DynamicImage, Label
from core.styles import Colors, Fonts
from core.data_sources import Local, WeatherData


class Weather(DynamicImage):
    def __init__(self, timeout):
        day_night = Local.day_night()
        condition = "clear" if self._conditions() == "Clear" else "cloudy"
        super().__init__(
            xy=(1208, 24), size=(688, 1112), timeout=timeout,
            img_url=f"./shared/images/weather-{condition}-{day_night}.png"
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
        temp = WeatherData.get_current()[0]
        return f"{temp}°C"

    @staticmethod
    def _conditions():
        cond = WeatherData.get_current()[1]
        return cond
