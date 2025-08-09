from core.elements import Widget, TextLabel, Icon
from shared.styles import Colors, Fonts
from core.data_sources import Local


class Weather(Widget):
    def __init__(self):
        self.current_data = {
            "main": {
                "temp": 19.81,
                "feels_like": 18.05
            },
            "weather": {
                "main": "Clear",
                "icon": "01d"
            },
            "clouds": {
                "all": 0
            }
        }
        self.hourly_data = {}
        self.bg_url = "./shared/images/weather/clear-day.png"
        super().__init__(
            xy=(1208, 24),
            size=(688, 1112),
            bg_url=self.bg_url
            )
        self.temp = TextLabel(
            xy=(90, 90),
            font=Fonts.WEATHER_TODAY,
            color=Colors.DEFAULT
        )
        self.contitions = TextLabel(
            xy=(90, 278),
            font=Fonts.LABEL_SMALL,
            color=Colors.SECONDARY
        )
        self.icon = Icon(xy=(470, 100), url="./shared/icons/weather/04d.png")
        self.hourly = Widget(
            size=(588, 640),
            xy=(50, 400),
            fill=(0, 0, 0, 80)
        )
        self.children = [
            self.hourly,
            self.temp,
            self.icon,
            self.contitions
        ]

    def _weather_image(self):
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

    def _temperature(self):
        temp = round(self.current_data["main"]["temp"])
        return f"{temp}°"

    def _current_icon(self):
        icon = self.current_data["weather"]["icon"]
        return f"./shared/icons/weather/{icon}.png"

    def _feels_like(self):
        temp = round(self.current_data["main"]["feels_like"])
        return f"Känner som {temp}°C"

    async def update(self):
        # Updating background image if needed
        # self.current_data = await WeatherData.fetch()
        # self.hourly_data = await WeatherData.fetch(False)

        new_url = self._weather_image()
        bg_dirty = False
        if new_url == self.bg_url:
            pass
        else:
            self.bg_url = new_url
            self.bg = self._get_image(self.bg_url)
            bg_dirty = True
        icon_dirty = self.icon.set_url(self._current_icon())
        temp_dirty = self.temp.set_text(self._temperature())
        cond_dirty = self.contitions.set_text(self._feels_like())

        if any((bg_dirty, icon_dirty, temp_dirty, cond_dirty)):
            await self.render()
            return True
        return False
