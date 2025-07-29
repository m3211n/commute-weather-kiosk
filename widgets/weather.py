from widgets.core import Widget, Label


class Weather(Widget):
    def __init__(self):
        super().__init__(position=(8, 964), size=(948, 1064))
        self.labelTime = Label()

    async def update_content(self) -> bool:
        return False

    async def render(self):
        self._clear()
