import asyncio
from PIL import Image, ImageDraw
from shared.styles import Colors, Fonts

class Widget:
    def __init__(self, name, interval=1, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self.interval = interval
        self.dirty = False
        self.x, self.y = position
        self.size = size
        self.bgcolor = bgcolor
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)
        self._draw_context.rounded_rectangle([(0, 0), self.size], radius=8, fill=self.bgcolor)
    
    def add_text(self, *args, **kwargs):
        box = self._draw_context.textbbox(args[0], args[1], font=kwargs.get("font"))
        self._draw_context.rectangle(box, fill=self.bgcolor)
        self._draw_context.text(*args, **kwargs)
    
    def add_image(self, path, coordinates):
        im = Image.open(path)
        box = coordinates[0], coordinates[1], coordinates[0] + im.width, coordinates[1] + im.height
        self.image.paste(im, box, mask=im.split()[3])
    
    async def callback(self):
        pass

    async def update(self):
        await self.callback()
        await asyncio.sleep(self.interval)



class Label:
    def __init__(self, text="Label", font=Fonts.value, position=(0, 0), anchor="la", fill=Colors.default):
        self.text = text
        self.font = font
        self.position = position
        self.fill = fill
        self.image = Image.new("RGBA", self.getbbox(), (0, 0, 0, 0))
        self.context = ImageDraw.Draw(self.image)
        self.anchor = anchor

    def getbbox(self):
        return self.font.getbbox(self.text)
    
    async def update(self, new_text):
        self.text = new_text
        self.image.paste((0, 0, 0, 0), [(0, 0), self.getbbox()])
        self.context.text((0, 0), self.text, self.fill, self.font, self.anchor)