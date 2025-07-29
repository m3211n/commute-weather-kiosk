from PIL import Image, ImageDraw
from datetime import datetime
from shared.styles import Fonts, Colors

class Widget:
    def __init__(self, name, interval=1, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self._interval = interval
        self.x, self.y = position
        self.size = size
        self.dirty = True
        self.bgcolor = bgcolor
        self.text_content = {}
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)
    
    async def update_content(self):
        return False

    async def render(self):
        if await self.update_content():
            self._draw_context.rounded_rectangle([(0, 0), self.size], radius=8, fill=self.bgcolor)
            for item in self.text_content.values():
                self._draw_context.text(**item.__dict__)
            self.dirty = True
        return self.dirty        



class Label:
    def __init__(self, text="Label", **kwargs):
        self.text = text
        for key, value in kwargs.items():
            setattr(self, key, value)



class Clock(Widget):

    TIME = "%H:%M"
    DATE = "%A, %B %d, , %Y"

    strf_now = lambda f: datetime.now().strftime(f)

    def __init__(self, interval=1):
        super().__init__("Clock", interval=interval, position=(8, 8), size=(948, 472))
        self._current_minute = -1
        self.text_content = {
            "time": Label(
                xy=(474, 268),
                text=Clock.strf_now(Clock.TIME),
                fill=Colors.default,
                font=Fonts.clock,
                anchor="mb"
            ),
            "date": Label(
                xy=(474, 300),
                text=Clock.strf_now(Clock.DATE),
                fill=Colors.title,
                font=Fonts.title,
                anchor="mt"
            )
        }
    
    async def update_content(self):
        if not self._current_minute == datetime.now().minute:
            self._current_minute = datetime.now().minute
            self.text_content["time"].text = Clock.strf_now(Clock.TIME)
            self.text_content["date"].text = Clock.strf_now(Clock.DATE)
            return True
        return False