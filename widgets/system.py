from widgets.core import Widget, Label
from shared.styles import Fonts, Colors


class System(Widget):
    def __init__(self):
        super().__init__(position=(8, 1120), size=(1904, 64))
        self.label = Label(
            xy=(20, 20),
            fill=Colors.TITLE,
            font=Fonts.STATUS
        )

    async def update_content(self) -> bool:
        from widgets.data_sources import get_system_info
        self.label.text = get_system_info()
        return True

    async def render(self):
        self._clear()
        await self.label.render_at(self.image)
