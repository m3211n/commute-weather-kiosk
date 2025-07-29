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
        self.content = {}
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
        for item in self.content.values():
            self.image.paste(item.image, item.bbox)
        await asyncio.sleep(self._interval)
        self.dirty = True


class Label:
    def __init__(self, text="Label", font=Fonts.value, position=(0, 0), anchor="la", fill=Colors.default, bg=Colors.panel_bg):
        self.text = text
        self.font = font
        self.size = self.bbox[2] - self.bbox[0], self.bbox[3] - self.bbox[1]
        self.position = position
        self.fill = fill
        self.bg = bg
        self.image = Image.new("RGB", self.size, self.bg)
        self.context = ImageDraw.Draw(self.image)
        self.anchor = anchor
    
    @property
    def bbox(self):
        return self.font.getbbox(self.text)

    async def update(self, new_text):
        self.text = new_text
        self.image.paste((0, 0, 0), self.bbox)
        self.context.text((0, 0), self.text, self.fill, self.font, self.anchor)