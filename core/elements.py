from shared.styles import Fonts, Colors
from core.render import Canvas, Fill, Image
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
            self, size=DEFAULT_SIZE, xy=(0, 0),
            fill=Colors.PANEL_BG, bg_url=None
            ):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(size=size)
        self.xy = xy
        self.children: List[Union[Widget, Content]] = []
        self._canvas: Canvas = Canvas(size, MODE)
        self._draw_canvas: Canvas = Canvas(size, MODE)
        if bg_url:
            self.bg = Image.open(bg_url)
        else:
            self.bg = Fill.color(self.size, mode=MODE, color=fill, radius=24)

    @property
    def canvas(self):
        return self._canvas()

    async def render(self):
        self._canvas.clear().paste(self.bg)
        self._draw_canvas.clear()
        for child in self.children:
            if isinstance(child, Widget):
                await child.render()
                self._canvas.paste(child.canvas, child.xy)
            elif isinstance(child, Icon):
                self._canvas.paste(**child.attr)
            elif isinstance(child, TextLabel):
                self._draw_canvas.draw.text(**child.attr)
            else:
                pass
        self._canvas.paste(self._draw_canvas())

    def update(self):
        raise NotImplementedError


class Content:
    def __init__(self, xy, attr):
        self.xy = xy
        self.attr = attr

    def update(self):
        raise NotImplementedError


class TextLabel(Content):
    def __init__(
            self, xy=(0, 0), text="", color=Colors.DEFAULT,
            font=Fonts.VALUE, anchor="lt"
            ):
        super().__init__(
            xy=xy,
            attr={
                "xy": xy,
                "text": text,
                "font": font,
                "fill": color,
                "anchor": anchor
            }
        )

    def update(self, text: str):
        """
        Changes the text of the label if new value is different from the
        current one. Returns True if text was updated and False if it wasn't.
        """
        if not text == self.attr["text"]:
            self.attr["text"] = text
            return True
        return False


class Icon(Content):
    def __init__(self, url, xy=(0, 0)):
        self.url = url
        super().__init__(
            xy=xy,
            attr={
                "xy": xy,
                "img": Image.open(self.url),
            }
        )

    def update(self, url: str):
        if not self.url == url:
            self.url = url
            self.attr["img"] = Image.open(self.url)
            return True
        return False
