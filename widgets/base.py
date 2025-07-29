import asyncio
from PIL import Image, ImageDraw
from shared.styles import Colors

class Widget:
    def __init__(self, name, interval=1, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self._interval = interval
        self.dirty = True
        self.x, self.y = position
        self.size = size
        self.bgcolor = bgcolor
        self.text_content = {}
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)
    
    async def callback(self):
        pass

    async def render(self):
        self._draw_context.rounded_rectangle([(0, 0), self.size], radius=8, fill=self.bgcolor)
        await self.callback()
        for item in self.text_content.values():
            self._draw_context.text(**item.__dict__)

    async def update(self):
        if not self.dirty:
            await self.render()
            self.dirty = True
            await asyncio.sleep(self._interval)



class Label:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
