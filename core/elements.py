from shared.styles import Fonts, Colors
from core.render import Canvas, Image
import inspect

DEFAULT_SIZE = (100, 100)
DEFAULT_RADIUS = 24
MODE = "RGBA"


class Container:
    def __init__(self, xy, size):
        self.xy = xy
        self.size = size
        self.children = []


class Widget(Container):
    def __init__(
            self, size=DEFAULT_SIZE, xy=(0, 0), fill=(0, 0, 0, 0), radius=0
            ):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(xy=xy, size=size)
        self.dirty = True
        self.fill = fill
        self.radius = radius
        self._canvas: Canvas = Canvas(size, MODE)
        self._draw_canvas: Canvas = Canvas(size, MODE)

    @property
    def canvas(self):
        return self._canvas()

    async def render(self):
        self._canvas.fill(self.fill, self.radius)
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

    async def update(self):
        for child in self.children:
            self.dirty = any((self.dirty, await child.update()))
        if self.dirty:
            await self.render()
            self.dirty = False
            return True
        return False


class Content:
    def __init__(self, xy, value_key, callback=None):
        self.xy = xy
        self.callback = callback if callback else self._dummy_callback
        self.value = None
        self.value_key = value_key
        self.attr = {
            "xy": self.xy,
            self.value_key: self.value
        }

    async def _dummy_callback(self):
        pass

    async def update(self):
        res = self.callback()
        new_value = await res if inspect.isawaitable(res) else res
        current = self.attr.get(self.value_key)
        if current != new_value:
            self.attr[self.value_key] = new_value
            return True
        return False


class TextLabel(Content):
    def __init__(
            self, xy=(0, 0), color=Colors.DEFAULT,
            font=Fonts.VALUE, anchor="lt", callback=None
            ):
        super().__init__(
            xy=xy,
            value_key="text",
            callback=callback
        )
        self.attr["font"] = font
        self.attr["fill"] = color
        self.attr["anchor"] = anchor


class Img(Content):
    def __init__(self, xy=(0, 0), callback=None):
        super().__init__(
            xy=xy,
            value_key="url",
            callback=callback
        )
