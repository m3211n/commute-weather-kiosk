from core.ui import ColorWidget, Label


class Dummy(ColorWidget):
    def __init__(self):
        super().__init__(xy=(8, 8), size=(948, 472))
        self.labelTime = Label()

    async def update_children(self) -> bool:
        return False

    async def render(self):
        self._clear()
