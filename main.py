import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
# from datetime import datetime
from screen import Screen
from rgb565fb import CanvasRGB565

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

canvas = CanvasRGB565(1920, 1200)

async def main():

    canvas.clear(0)
    canvas.draw_rect(300, 300, 100, 100, 0xFFF0)
    canvas.draw_text(400, 400, "Hello Hacker!", "fonts/chicago.bdf", 15, 0xFFF0)

    with Screen() as s:
        for i, color in enumerate(((127, 0, 0), (0, 127, 0), (0, 0, 127))):
            s.add(Widget(f"test_{i}", (i*200, 0), (200, 100), color))

        while True:
            for widget in s.widgets.values():
                widget.clean()
                widget.text((0, 0), f"{widget.name}", font=fnt_16, fill=(255, 255, 255))
                widget.text((0, 20), f"{random.randint(1000, 9999)}", font=fnt_40, fill=(255, 255, 255))
            
            await s.refresh_all()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())