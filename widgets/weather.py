from widgets.core import Widget, Label


class Weather(Widget):
    def __init__(self):
        super().__init__(position=(964, 8), size=(948, 1064))
        self.labelTime = Label()

    async def update_content(self) -> bool:
        return True

    async def render(self):
        self._clear()
