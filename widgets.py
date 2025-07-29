from PIL import Image, ImageDraw
from datetime import datetime
from shared.styles import Fonts, Colors


class Widget:
    """Generic widget class"""
    def __init__(
            self, name,
            position=(0, 0),
            size=(100, 100),
            bgcolor=Colors.panel_bg):

        self.name = name
        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.content = {}
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)

    async def update_content(self):
        return False

    async def render(self):
        if await self.update_content():
            self._draw_context.rounded_rectangle(
                [(0, 0), self.size],
                radius=8,
                fill=self.bgcolor
            )
            for item in self.content.values():
                if isinstance(item, Label):
                    self._draw_context.text(**item.__dict__)
            return True
        return False


class Label:
    """Generic label class"""
    def __init__(self, text="Label", **kwargs):
        self.text = text
        for key, value in kwargs.items():
            setattr(self, key, value)


class Clock(Widget):
    """Clock widget"""
    TIME = "%H:%M"
    DATE = "%A, %B %d, %Y"

    def __init__(self):
        super().__init__(
            "Clock",
            position=(8, 8),
            size=(948, 472)
        )
        self._current_minute = -1
        self.content = {
            "time": Label(
                xy=(474, 268),
                text=self.strf_now(Clock.TIME),
                fill=Colors.default,
                font=Fonts.clock,
                anchor="mb"
            ),
            "date": Label(
                xy=(474, 300),
                text=self.strf_now(Clock.DATE),
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
            )
        }

    def strf_now(self, f):
        return datetime.now().strftime(f)

    async def update_content(self):
        if not self._current_minute == datetime.now().minute:
            self._current_minute = datetime.now().minute
            self.text_content["time"].text = self.strf_now(Clock.TIME)
            self.text_content["date"].text = self.strf_now(Clock.DATE)
            return True
        return False
