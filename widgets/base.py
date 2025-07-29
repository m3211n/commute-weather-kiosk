import asyncio
from PIL import Image, ImageDraw
from shared.styles import Colors, Fonts

class Widget:
    def __init__(self, name, interval=1, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self._interval = interval
        self.dirty = False
        self.x, self.y = position
        self.size = size
        self.bgcolor = bgcolor
        self.text_content = {}
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)
        self._draw_context.rounded_rectangle([(0, 0), self.size], radius=8, fill=self.bgcolor)
    
    async def callback(self):
        pass

    async def start(self):
        await self.callback()
        self.dirty = True

    async def update(self):
        if not self.dirty:
            await self.callback()
        for item in self.text_content.values():
            self._draw_context.text(**item)
        await asyncio.sleep(self._interval)
        self.dirty = True


class Label:
    def __init__(self, xy=(0, 0), text="Label", fill=Colors.default, font=Fonts.value, anchor="la"):
        self._text = text
        self.font = font
        self.xy = xy
        self.fill = fill
        self.anchor = anchor

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text
