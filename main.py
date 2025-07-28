import asyncio
import random
from PIL import Image, ImageDraw
# from datetime import datetime
from screen import Screen
from shared.styles import Fonts, Colors

class Widget:
    def __init__(self, name, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self.x, self.y = position
        self.w, self.h = size
        self.bgcolor = bgcolor
        self.image = Image.new("RGB", (self.w, self.h), self.bgcolor)
        self._draw_context = ImageDraw.Draw(self.image)

    def get_image(self):
        return self.image
    
    def clean(self):
        self._draw_context.rounded_rectangle([0, 0, self.w, self.h], radius=8, fill=self.bgcolor)

    def text(self, *args, **kwargs):
        box = self._draw_context.textbbox(args[0], args[1], font=kwargs.get("font"))
        self._draw_context.rectangle(box, fill=self.bgcolor)
        self._draw_context.text(*args, **kwargs)
    
    def add_image(self, path, coordinates):
        im = Image.open(path)
        box = coordinates[0], coordinates[1], coordinates[0] + im.width, coordinates[1] + im.height
        self.image.paste(im, box, mask=im.split()[3])

widgets = {
    Widget("Clock", (8, 8), (948, 400)),
    Widget("Trains_1", (8, 416), (948, 200)),
    Widget("Trains_2", (8, 624), (948, 200)),
    Widget("Busses_1", (8, 832), (948, 200)),
    Widget("Weather", (964, 8), (948, 1064)),
    Widget("Status", (8, 1032), (1904, 160))
}


async def main():
    with Screen() as s:
        s.add(widgets)
        await s.clear()
        s.widgets["Weather"].add_image("shared/weather_icons/cloudy.png", (200, 200))
        bulk = False
        while True:
            for widget in s.widgets.values():
                widget.text((8, 8), f"{widget.name}", font=Fonts.title, fill=Colors.title)
                widget.text((8, 40), f"{random.randint(1000, 9999)}", font=Fonts.value, fill=Colors.default)
                widget.text((8, 120), f"{random.randint(1000, 9999)}", font=Fonts.clock, fill=Colors.departure_times)
            if bulk:
                await s.refresh_all_bulk()
            else:
                await s.refresh_all()
            bulk = not bulk
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())