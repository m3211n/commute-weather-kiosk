import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
# from datetime import datetime
from screen import Screen

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

class Widget:
    def __init__(self, name, position=(0, 0), size=(100, 100), bgcolor=(0, 0, 0)):
        self.name = name
        self.x, self.y = position
        self.w, self.h = size
        self.bgcolor = bgcolor
        self.image = Image.new("RGB", (self.w, self.h), self.bgcolor)
        self._draw_context = None
    
    def get_context(self, clean=True):
        self._draw_context = ImageDraw.Draw(self.image)
        if clean:
            self._draw_context.rectangle([0, 0, self.w, self.h], fill=self.bgcolor)
        return self._draw_context

    def get_image(self):
        return self.image
      
async def main():

    with Screen() as s:
        for i, color in enumerate(((255, 0, 0), (0, 255, 0), (0, 0, 255))):
            s.add(Widget(f"test_{i}", (i*100, 0), (100, 100), color))
        await s.clear()

        while True:
            for widget in s.widgets.values():
                context = widget.get_context()
                context.text((0, 0), f"{random.randint(1000, 9999)}", font=fnt, fill=(255, 255, 255))
            
            await s.refresh_all()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())