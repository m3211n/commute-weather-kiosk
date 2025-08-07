from core.widget import Widget, ImageWidget, TextWidget
from core.styles import Colors, Fonts
from core.data_sources import WeatherData, Local


class Weather(Widget):
    def __init__(self, interval=900):
        super().__init__(
            position=(1208, 24),
            size=(688, 1112),
            fill=Colors.NONE,
            interval=interval
            )
        self.current_data = {
            "main": {
                "temp": 24.55
            },
            "weather": {
                "main": "Clear"
            }
        }
        self.hourly_data = {}
        self.background = ImageWidget(
                url="./shared/images/weather/clear-day.png",
                update_callback=self._get_image,
                interval=interval
            )
        self.temp = TextWidget(
                update_callback=self._temperature,
                position=(90, 90),
                font=Fonts.WEATHER_TODAY,
                color=Colors.DEFAULT
            )
        self.contitions = TextWidget(
                update_callback=self._conditions,
                position=(90, 210),
                font=Fonts.LABEL_SMALL,
                color=Colors.SECONDARY
            )

    def _get_image(self):
        weather = self.current_data["weather"]
        c = "clear" if weather["main"] == "Clear" else "clouds"
        d = Local.day_or_night()
        # icon = weather["icon"]
        return f"./shared/images/weather/{c}-{d}.png"

    def _temperature(self):
        temp = round(self.current_data["main"]["temp"], 1)
        return f"{temp}°"

    def _conditions(self):
        return self.current_data["weather"]["main"]

    async def update(self):
        self.background.render()
        self.current_data = await WeatherData.fetch()
        self.hourly_data = await WeatherData.fetch(False)
