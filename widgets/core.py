from PIL import Image, ImageDraw
from shared.styles import Fonts, Colors
from typing import List


class Content():
    """Generic class for dynamically updated content"""
    async def update(self):
        return False


class Label(Content):
    """Generic label class.
    Uses the same attributes as PIL.ImageDraw.Draw.text"""
    def __init__(self, xy=(0, 0), text="Label", fill=Colors.default,
                 font=Fonts.value, anchor="la", callback=None):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font = font
        self.anchor = anchor
        self.callback = callback

    async def update(self):
        return await super().update()


class Widget:
    """Generic widget class"""
    def __init__(
            self,
            position=(0, 0),
            size=(100, 100),
            bgcolor=Colors.panel_bg,
            radius=16,
            content: List[Content] = []):

        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.radius = radius
        self.content = content
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)

    def _clear(self):
        self._draw_context.rounded_rectangle(
            [(0, 0), self.size],
            radius=self.radius,
            fill=self.bgcolor
        )

    async def update_content(self) -> bool:
        return any([await item.update() for item in self.content])

    async def maybe_render(self) -> bool:
        if await self.update_content():
            # Render and convert to RGB565
            self._clear()
            for item in self.content:
                if isinstance(item, Label):
                    self._draw_context.text(**item.__dict__)
            return True
        return False
