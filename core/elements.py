from shared.styles import Fonts, Colors
from core.render import Canvas
from PIL import Image, ImageDraw
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
        self.canvas: Canvas = Canvas(size, MODE)
        self._draw_canvas: Canvas = Canvas(size, MODE)
        self.bg = self._get_image(bg_url) if bg_url else self._get_color(fill)

    async def render(self):
        self.canvas.clear().paste(self.bg)
        for child in self.children:
            if isinstance(child, Widget):
                await child.render()
                self.canvas.paste(child.canvas, child.xy)
            elif isinstance(child, Icon):
                self.canvas.paste(**child.attr)
            elif isinstance(child, TextLabel):
                self._draw_canvas.draw.text(**child.attr)
            else:
                pass
        self.canvas.paste(self._draw_canvas)

    def update(self):
        raise NotImplementedError

    def _get_color(self, fill) -> Image.Image:
        img = Image.new(MODE, self.size)
        draw = ImageDraw.Draw(img)
        xy = self.xy if self._parent else (0, 0)
        draw.rounded_rectangle(
            [*xy, *self.size], radius=DEFAULT_RADIUS, fill=fill
            )
        return img

    def _get_image(self, url) -> Image.Image:
        img = Image.open(url, mode="r")
        return img

    def _clear(self):
        self._draw_canvas = Image.new(MODE, self.size)
        self.canvas = Image.new(MODE, self.size)


class Content:
    def __init__(self, xy):
        self.xy = xy
        self.attr = {}

    def update(self):
        raise NotImplementedError


class TextLabel(Content):
    def __init__(
            self, xy=(0, 0), text="", color=Colors.DEFAULT,
            font=Fonts.VALUE, anchor="lt"
            ):
        super().__init__(xy=xy)
        # Draws text on transparent image of same size as parent widget
        self.attr = {
            "xy": xy,
            "text": text,
            "font": font,
            "fill": color,
            "anchor": anchor
        }

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
        super().__init__(xy=xy)
        self.url = url
        self.attr = {
            "xy": xy,
            "img": Image.open(self.url)
        }

    def update(self, url):
        if not self.url == url:
            self.url = url
            self.attr["img"] = Image.open(self.url)
            return True
        return False
