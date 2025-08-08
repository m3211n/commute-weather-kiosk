from core.elements import Widget, TextLabel
from core.styles import Fonts, Colors
# from core.data_sources import Commute


class Departures(Widget):
    def __init__(self, xy, title="Departures"):
        self.title_text = title
        super().__init__(
            xy=xy,
            size=(1160, 368))
        self.title = TextLabel(
            xy=(32, 32),
            color=Colors.TITLE,
            font=Fonts.LABEL_SMALL
        )
        self.children = [
            self.title
        ]

    async def update(self):
        if self.title.update(text=self.title_text):
            await self.render()
        return False


class Trains(Departures):
    def __init__(self):
        super().__init__(xy=(24, 376), title="Pendeltåg mot City")


class Busses(Departures):
    def __init__(self):
        super().__init__(xy=(24, 768), title="Buss mot Jakobsberg Stn.")
