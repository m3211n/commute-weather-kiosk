from core.ui import Widget, Text, ImageView
from core.styles import Colors, Fonts
from __archive.__store import Store


class Hourly(Widget):
    def __init__(self, store: Store):
        super().__init__(
            store=store, sub_key="hourly",
            size=(588, 640),
            xy=(50, 400),
            fill=(0, 0, 0, 80),
            radius=48
        )
        self.content = {
            "time": Text((40, 40), font=Fonts.LABEL_SMALL),
            "value": Text((200, 40), font=Fonts.LABEL_SMALL)
        }


class Weather(Widget):
    def __init__(self, store: Store):
        super().__init__(
            store=store, sub_key="weather",
            xy=(1208, 24), size=(688, 1112)
            )
        self._cached = {
            "weather_image": "./shared/images/weather/clear-night.png",
            "hourly": {
                "time": "18:00",
                "value": "Hello there!"
            },
            "temp": "19°",
            "icon": "./shared/icons/weather/01n.png",
            "feels_like": "Känner som 12°C"
        }
        self.content = {
            "weather_image": ImageView(),
            "hourly": Hourly(self.store),
            "temp": Text(
                xy=(90, 90), font=Fonts.H1, color=Colors.DEFAULT
            ),
            "icon": ImageView(xy=(470, 100)),
            "feels_like": Text(
               xy=(90, 278), font=Fonts.LABEL_SMALL, color=Colors.SECONDARY
            )
        }
