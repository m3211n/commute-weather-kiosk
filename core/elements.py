from shared.styles import Fonts, Colors
from core.render import Canvas, Image
from typing import List, Union


DEFAULT_SIZE = (100, 100)
DEFAULT_RADIUS = 24
MODE = "RGBA"


class Container:
    def __init__(self, size):
        self.size = size
        self._children = []


class Widget(Container):
    def __init__(
            self, size=DEFAULT_SIZE, xy=(0, 0), fill=(0, 0, 0, 0), radius=0
            ):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(size=size)
        self.xy = xy
        self.fill = fill
        self.radius = radius
        self.children: List[Union[Widget, Content]] = []
        self._canvas: Canvas = Canvas(size, MODE)
        self._draw_canvas: Canvas = Canvas(size, MODE)

    @property
    def canvas(self):
        return self._canvas()

    async def render(self):
        self._canvas.clear()
        self._draw_canvas.clear()
        for child in self.children:
            if isinstance(child, Widget):
                await child.render()
                self._canvas.paste(child.canvas, child.xy)
            elif isinstance(child, Img):
                img = Image.open(child.attr[child.value_key])
                self._canvas.paste(img, child.xy)
            elif isinstance(child, TextLabel):
                self._draw_canvas.draw.text(**child.attr)
            else:
                pass
        self._canvas.paste(self._draw_canvas())

    def update(self):
        raise NotImplementedError


class Content:
    def __init__(self, xy, value_key, value):
        self.xy = xy
        self.value = value
        self.value_key = value_key
        self.attr = {
            "xy": self.xy,
            self.value_key: self.value
        }

    def set_value(self, new_value):
        if not self.attr[self.value_key] == new_value:
            self.attr[self.value_key] = new_value
            return True
        return False


class TextLabel(Content):
    def __init__(
            self, xy=(0, 0), text="", color=Colors.DEFAULT,
            font=Fonts.VALUE, anchor="lt"
            ):
        super().__init__(
            xy=xy,
            value=text,
            value_key="text"
        )
        self.attr["font"] = font
        self.attr["fill"] = color
        self.attr["anchor"] = anchor


class Img(Content):
    def __init__(self, url, xy=(0, 0)):
        super().__init__(
            xy=xy,
            value=url,
            value_key="url"
        )
