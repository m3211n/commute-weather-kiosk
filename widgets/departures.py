from core.elements import Widget, TextLabel
from core.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(Widget):
    async def __init__(self, xy, title="Departures"):
        super().__init__(
            xy=xy,
            size=(1160, 368))
        self.title = TextLabel(
            xy=(32, 32),
            text=title,
            color=Colors.TITLE,
            font=Fonts.LABEL_SMALL
        )
        self.children = [
            self.title
        ]
        await self.title.render()

    async def maybe_update(self):
        await self.render()
        return False


class Trains(Departures):
    def __init__(self):
        super().__init__(xy=(24, 376), title="Pendeltåg mot City")


class Busses(Departures):
    def __init__(self):
        super().__init__(xy=(24, 768), title="Buss mot Jakobsberg Stn.")
