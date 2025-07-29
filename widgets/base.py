from PIL import Image, ImageDraw
from shared.styles import Colors

class Widget:
    def __init__(self, name, interval=1, position=(0, 0), size=(100, 100), bgcolor=Colors.panel_bg):
        self.name = name
        self._interval = interval
        self.x, self.y = position
        self.size = size
        self.bgcolor = bgcolor
        self.text_content = {}
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)
    
    async def update_content(self):
        return False

    async def render(self):
        if await self.update_content():
            self._draw_context.rounded_rectangle([(0, 0), self.size], radius=8, fill=self.bgcolor)
            for item in self.text_content.values():
                self._draw_context.text(**item.__dict__)
            return True # Dirty Flag
        else:
            return False # Dirty Flag
        


class Label:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
