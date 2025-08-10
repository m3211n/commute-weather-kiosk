from core.elements import Widget, TextLabel, Img
from shared.styles import Colors, Fonts
from core.data_sources import Local


class Weather(Widget):
    def __init__(self):
        self.current_data = {
            "main": {
                "temp": 18.58,
                "feels_like": 18.22
            },
            "weather": {
                "main": "Clouds",
                "icon": "03d"
            },
            "clouds": {
                "all": 40
            }
        }
        self.hourly_data = {}
        self.time_cond = ""
        super().__init__(xy=(1208, 24), size=(688, 1112))
        self.bg = Img(callback=self._weather_image)
        self.temp = TextLabel(
            xy=(90, 90),
            font=Fonts.WEATHER_TODAY,
            color=Colors.DEFAULT,
            callback=self._temperature
        )
        self.feels_like = TextLabel(
            xy=(90, 278),
            font=Fonts.LABEL_SMALL,
            color=Colors.SECONDARY,
            callback=self._feels_like
        )
        self.cond_icon = Img(
            xy=(470, 100),
            callback=self._current_icon
        )
        self.hourly = Widget(
            size=(588, 640),
            xy=(50, 400),
            fill=(0, 0, 0, 80),
            radius=48
        )
        self.children = [
            self.bg,
            self.hourly,
            self.temp,
            self.cond_icon,
            self.feels_like
        ]

    async def _weather_image(self):
        clouds = self.current_data["clouds"]["all"]
        if clouds in range(0, 33):
            c = "clear"
        elif clouds in range(33, 66):
            c = "cloudy"
        else:
            c = "rainy"
        d = Local.day_or_night()
        # icon = weather["icon"]
        return f"./shared/images/weather/{c}-{d}.png"

    async def _temperature(self):
        temp = round(self.current_data["main"]["temp"])
        return f"{temp}°"

    async def _current_icon(self):
        icon = self.current_data["weather"]["icon"]
        return f"./shared/icons/weather/{icon}.png"

    async def _feels_like(self):
        temp = round(self.current_data["main"]["feels_like"])
        return f"Känner som {temp}°C"
