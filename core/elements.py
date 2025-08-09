from shared.styles import Fonts, Colors
from PIL import Image, ImageDraw
from typing import List
import logging


DEFAULT_SIZE = (100, 100)
DEFAULT_RADIUS = 24
MODE = "RGBA"


class Container:
    def __init__(self, size):
        self.size = size
        self._parent = None
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
        self._parent: Widget = None
        self._children: List[Widget] = []
        self._canvas: Image.Image = None
        self.bg = self._get_image(bg_url) if bg_url else self._get_color(fill)

    @property
    def children(self) -> List[Container]:
        return self._children

    @children.setter
    def children(self, new_children: List[Container] = []):
        self._children = []
        if len(new_children) > 0:
            for child in new_children:
                child._parent = self
                child.size = self.size
                self._children.append(child)

    @property
    def canvas(self) -> Image.Image:
        return self._canvas

    async def render(self):
        self._canvas = self._clear() if self._parent else self._clear(True)
        self._canvas.paste(self.bg, mask=self.bg.split()[3])
        for child in self._children:
            await child.render()
            self._canvas.paste(
                child._canvas,
                (0, 0),
                mask=child._canvas.split()[3]
            )

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

    def _clear(self, solid=False):
        color = (0, 0, 0, 255) if solid else (0, 0, 0, 0)
        return Image.new(MODE, self.size, color=color)


class TextLabel(Widget):
    def __init__(
            self, xy, text="", color=Colors.DEFAULT,
            font=Fonts.VALUE, anchor="lt"
            ):
        super().__init__(xy=xy, fill=(0, 0, 0, 0))
        # Draws text on transparent image of same size as parent widget
        self.color = color
        self.font = font
        self.anchor = anchor
        self.text = text

    def set_text(self, text: str):
        """
        Changes the text of the label if new value is different from the
        current one. Returns True if text was updated and False if it wasn't.
        """
        if not text == self.text:
            self.text = text
            return True
        return False

    async def render(self):
        """Renders the image based on the current text unconditionally."""
        self._canvas = self._clear()
        logging.debug("Rendering text: %s", self.text)
        ImageDraw.Draw(self._canvas).text(
            self.xy, self.text, font=self.font, fill=self.color,
            anchor=self.anchor)


class Icon(Widget):
    def __init__(self, url, xy=(0, 0)):
        super().__init__(xy=xy)
        self.url = url

    def set_url(self, url):
        if not self.url == url:
            self.url = url
            return True
        return False

    async def render(self):
        self._canvas = self._clear()
        self._canvas.paste(Image.open(self.url), self.xy)
