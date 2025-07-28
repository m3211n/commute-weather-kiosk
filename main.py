import asyncio
import random
from PIL import Image, ImageDraw
# from datetime import datetime
from screen import Screen
from shared.fonts import Fonts

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
    Widget("Clock", (8, 8), (948, 560), (56, 28, 56)),
    Widget("Trains_1", (8, 576), (948, 200), (56, 28, 56)),
    Widget("Trains_2", (8, 784), (948, 200), (56, 28, 56)),
    Widget("Busses_1", (8, 992), (948, 200), (56, 28, 56)),
    Widget("Vaginas", (964, 8), (948, 1192), (56, 28, 56))
}


async def main():
    with Screen() as s:
        s.add(widgets)
        await s.clear()
        while True:
            for widget in s.widgets.values():
                widget.clean()
                widget.text((8, 8), f"{widget.name}", font=Fonts.title, fill=(255, 255, 255))
                widget.text((8, 20), f"{random.randint(1000, 9999)}", font=Fonts.value_small, fill=(255, 255, 255))      
            await s.refresh_all()
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())