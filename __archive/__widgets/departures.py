from core.ui import Widget, Text
from core.styles import Fonts, Colors
from __archive.__store import Store
# from core.data_sources import Commute


class Departures(Widget):
    def __init__(self, store: Store):
        super().__init__(
            store=store, sub_key="commute",
            xy=(24, 376),
            size=(1160, 468)
        )
        self._cached = {
            "trains": {
                "title": "Pendeltåg",
                "direction": "Stockholm City"
            },
            "buses": {
                "title": "Buss",
                "direction": "Jakobsbergs Station"
            }
        }
        self.trains = Widget(
            store=self.store,
            sub_key="trains",
            xy=(0, 0),
            size=(568, 468),
            fill=Colors.PANEL_BG,
            radius=24
        )
        self.trains.content = {
            "title": Text(
                xy=(40, 40),
                font=Fonts.LABEL_SMALL,
                color=Colors.TETRIARY
            ),
            "direction": Text(
                xy=(40, 84),
                font=Fonts.LABEL_SMALL,
                color=Colors.DEFAULT
            ),
        }
        self.buses = Widget(
            store=self.store,
            sub_key="buses",
            xy=(592, 0),
            size=(568, 468),
            fill=Colors.PANEL_BG,
            radius=24
        )
        self.buses.content = {
            "title": Text(
                xy=(40, 40),
                font=Fonts.LABEL_SMALL,
                color=Colors.TETRIARY
            ),
            "direction": Text(
                xy=(40, 84),
                font=Fonts.LABEL_SMALL,
                color=Colors.DEFAULT
            ),
        }
        self.content = {
            "trains": self.trains,
            "buses": self.buses
        }
