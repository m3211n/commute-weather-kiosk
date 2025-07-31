from widgets.data_sources import Tools
from core.ui import Widget, Label
from shared.styles import Colors, Fonts


class Weather(Widget):
    def __init__(self, timeout=900):
        super().__init__(position=(1208, 24), size=(688, 1112))
        self.labelTemperature = Label(
            xy=(90, 90),
            font=Fonts.WEATHER_TODAY,
            fill=Colors.DEFAULT,
            anchor="lt"
        )
        self.labelConditions = Label(
            xy=(90, 120),
            font=Fonts.WEATHER_TODAY,
            fill=Colors.TITLE,
            anchor="lt"
        )
        self.timeout = timeout
        self._next_update = Tools.time()

    async def update_content(self) -> bool:
        self.labelTemperature.text = "24°C"
        self.labelConditions.text = "Clear"
        return self._update_timeout()

    async def render(self):
        self._clear()
        await self.labelTemperature.render_at(self.image)
        await self.labelConditions.render_at(self.image)
