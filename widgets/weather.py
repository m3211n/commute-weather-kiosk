from core.ui import Widget, ImageWidget, TextWidget
from core.styles import Colors, Fonts
from core.data_sources import WeatherData, Local


class Weather(Widget):
    async def __init__(self, interval=900):
        super().__init__(
            position=(1208, 24),
            size=(688, 1112),
            fill=Colors.NONE,
            interval=interval
            )
        self.children = [
            ImageWidget(
                url="./shared/images/weather/clear-day.png",
                update_callback=self._get_image,
                interval=interval
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
        self.current_data = await WeatherData.fetch()
        self.hourly_data = await WeatherData.fetch(False)

    def _get_image(self):
        weather = self.current_data["weather"]
        c = "clear" if weather["main"] == "Clear" else "clouds"
        d = Local.day_or_night()
        # icon = weather["icon"]
        return f"./shared/images/weather/{c}-{d}.png"

    def _temperature(self):
        main = self.current_data["main"]
        temp = round(main["temp"], 1)
        return f"{temp}°"

    def _conditions(self):
        return self.current_data["weather"]["main"]
