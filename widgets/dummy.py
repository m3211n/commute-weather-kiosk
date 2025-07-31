from core.ui import Widget, Label


class Dummy(Widget):
    def __init__(self):
        super().__init__(position=(8, 8), size=(948, 472))
        self.labelTime = Label()

    async def update_content(self) -> bool:
        return False

    async def render(self):
        self._clear()
