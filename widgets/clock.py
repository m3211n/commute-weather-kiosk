from widgets.data_sources import get_time
from widgets.core import Widget, Label
from shared.styles import Colors, Fonts

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%A, %B %d, %Y"


class Clock(Widget):
    def __init__(self):
        super().__init__(
            position=(8, 8),
            radius=(64, 64, 16, 16),
            size=(948, 548)
            )
        self.labelTime = Label(
            xy=(474, 314),
            font=Fonts.CLOCK,
            anchor="mb"
        )
        self.labelDate = Label(
            xy=(474, 336),
            fill=Colors.SECONDARY,
            font=Fonts.TITLE,
            anchor="mt"
        )

    async def update_content(self):
        current_time = get_time(TIME_FORMAT)
        if self.labelTime.text != current_time:
            self.labelTime.text = current_time
            self.labelDate.text = get_time(DATE_FORMAT)
            return True
        return False

    async def render(self):
        self._clear()
        await self.labelTime.render_at(self.image)
        await self.labelDate.render_at(self.image)
