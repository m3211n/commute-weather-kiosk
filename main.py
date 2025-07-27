import asyncio
import random
from PIL import Image, ImageDraw, ImageFont
# from datetime import datetime
from screen import Screen

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

class Widget:
    def __init__(self, name, position=(0, 0), size=(100, 100), bgcolor="black"):
        self.name = name
        self.x, self.y = position
        self.w, self.h = size
        self.image = Image.new("RGB", (self.w, self.h), bgcolor)
        self._draw_context = ImageDraw.Draw(self.image)
    
    def get_context(self):
        return self._draw_context
      
async def main():

    with Screen() as s:
        for i, color in enumerate(("red", "green", "blue")):
            s.add(Widget("test", (i*100, 0), (100, 100), color))

    while True:
        for widget in s.widgets.values():
            context = widget.get_context()
            context.text((0, 0), f"{random.randint(1000, 9999)}", fnt, "white")
        
        await s.refresh_all()
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())