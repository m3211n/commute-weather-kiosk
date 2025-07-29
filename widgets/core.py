from PIL import Image, ImageDraw
from shared.styles import Fonts, Colors


class Widget:
    """Generic widget class"""
    def __init__(
            self,
            position=(0, 0),
            size=(100, 100),
            bgcolor=Colors.panel_bg,
            content=[]):

        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.content = content
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)

    def is_up_to_date(self) -> bool:
        if any(item.callback() for item in self.content):
            return True
        return False

    def render(self) -> bool:
        if self.is_up_to_date():
            self._draw_context.rounded_rectangle(
                [(0, 0), self.size],
                radius=8,
                fill=self.bgcolor
            )
            for item in self.content:
                if isinstance(item, Label):
                    self._draw_context.text(**item.__dict__)
            return True
        return False


class Label:
    """Generic label class.
    Uses the same attributes as PIL.ImageDraw.Draw.text"""

    def _default_callback():
        return False

    def __init__(
            self,
            xy=(0, 0),
            text="Label",
            fill=Colors.default,
            font=Fonts.value,
            anchor="la",
            callback=None):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font = font
        self.anchor = anchor
        self.callback = callback
