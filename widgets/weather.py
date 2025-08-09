from core.elements import Widget, TextLabel, Icon
from core.styles import Colors, Fonts
from core.data_sources import Local


class Weather(Widget):
    def __init__(self):
        self.current_data = {
            "main": {
                "temp": 24.55
            },
            "weather": {
                "main": "Clear",
                "icon": "01d"
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
            xy=(90, 210),
            font=Fonts.LABEL_SMALL,
            color=Colors.SECONDARY
        )
        self.icon = Icon(xy=(470, 100), url="./shared/icons/weather/04d.png")
        self.hourly = Widget()
        self.children = [
            self.temp,
            self.icon,
            self.contitions
        ]

    def _weather_image(self):
        cond = self.current_data["weather"]["main"]
        c = "clear" if cond == "Clear" else "clouds"
        d = Local.day_or_night()
        # icon = weather["icon"]
        return f"./shared/images/weather/{c}-{d}.png"

    def _temperature(self):
        temp = round(self.current_data["main"]["temp"], 1)
        return f"{temp}°"

    def _current_icon(self):
        icon = self.current_data["weather"]["icon"]
        return f"./shared/icons/weather/{icon}.png"

    def _conditions(self):
        return self.current_data["weather"]["main"]

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
        icon_dirty = self.icon.update(self._current_icon())
        temp_dirty = self.temp.update(self._temperature())
        cond_dirty = self.contitions.update(self._conditions())

        if any((bg_dirty, icon_dirty, temp_dirty, cond_dirty)):
            return True
        return False
