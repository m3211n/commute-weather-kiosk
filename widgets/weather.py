from widgets.data_sources import Tools
from core.ui import Widget, Label


class Weather(Widget):
    def __init__(self, timeout=900):
        super().__init__(position=(964, 8), size=(948, 1128))
        self.label = Label()
        self.timeout = timeout
        self._next_update = Tools.time()

    async def update_content(self) -> bool:
        return self._update_timeout()

    async def render(self):
        self._clear()
        await self.label.render_at(self.image)
