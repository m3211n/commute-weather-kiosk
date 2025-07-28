import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
# from datetime import datetime
from screen import Screen

fnt_40 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
fnt_16 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)

class Widget:
    def __init__(self, name, position=(0, 0), size=(100, 100), bgcolor=(0, 0, 0)):
        self.name = name
        self.x, self.y = position
        self.w, self.h = size
        self.bgcolor = bgcolor
        self.image = Image.new("RGB", (self.w, self.h), self.bgcolor)
        self._draw_context = ImageDraw.Draw(self.image)

    def get_image(self):
        return self.image
    
    def clean(self):
        self._draw_context.rectangle([0, 0, self.w, self.h], fill=self.bgcolor)

    def text(self, *args, **kwargs):
        self._draw_context.text(*args, **kwargs)

widgets = {
    Widget("Nipples", (0, 0), (200, 200), (100, 0, 0)),
    Widget("Penises", (200, 0), (200, 200), (0, 100, 0)),
    Widget("Vaginas", (400, 0), (200, 200), (0, 0, 100))
}


async def main():
    with Screen() as s:
        s.add(widgets)
        await s.clear()
        while True:
            for widget in s.widgets.values():
                widget.clean()
                widget.text((8, 8), f"{widget.name}", font=fnt_16, fill=(255, 255, 255))
                widget.text((8, 20), f"{random.randint(1000, 9999)}", font=fnt_40, fill=(255, 255, 255))      
            await s.refresh_all()
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())