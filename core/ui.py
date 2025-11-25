from PIL import Image, ImageDraw
from core.styles import Colors
from typing import Dict, Tuple
from abc import ABC, abstractmethod

DEFAULT_CONTAINER = (100, 100)
DEFAULT_RADIUS = 24


class Canvas:
    def __init__(self, size, mode="RGBA"):
        self._mode = mode
        self._img = Image.new(mode=self._mode, size=size, color=(0, 0, 0, 0))

    def __call__(self) -> Image.Image:
        return self._img

    def clear(self) -> "Canvas":
        size = self._img.size
        self._img = Image.new(mode=self._mode, size=size)
        return self

    def fill(self, color=(0, 0, 0, 0), radius=0) -> "Canvas":
        if radius != 0:
            self.draw.rounded_rectangle(
                [0, 0, *self._img.size],
                radius=radius,
                fill=color
            )
        else:
            self._img = Image.new(
                mode=self._mode, size=self._img.size, color=color)
        return self

    def paste(self, img: Image.Image, xy=(0, 0)):
        # import datetime
        # print("Pasting image. Mode is", img.mode)
        # f = f"{datetime.datetime.now().timestamp() * 1000}"
        # img.save(f"__preview/output{f}.png", format="png")
        mask = img.split()[3]
        self._img.paste(img, xy, mask=mask)

    def copy(self) -> "Canvas":
        copy = Canvas(self._img.size, self._mode)
        copy._img = self._img.copy()
        return copy

    def paste_from_url(self, url, xy=(0, 0)) -> "Canvas":
        img = Image.open(url)
        self._img.paste(img, xy)
        return self

    async def asRGB565(self):
        from numpy import asarray, uint16
        """Convert image from RGB888 to RGB565
        for /dev/fb0 on Pi Zero 2W"""
        # Flatten RGBA image
        arr = asarray(self._img)
        arr16 = arr.astype(uint16)
        r = (arr16[:, :, 0] & 0xF8) << 8         # 5 bits
        g = (arr16[:, :, 1] & 0xFC) << 3         # 6 bits
        b = (arr16[:, :, 2] & 0xF8) >> 3         # 5 bits
        rgb565 = r | g | b
        # little-endian for /dev/fb0
        return rgb565.astype('<u2').tobytes()

    @property
    def draw(self):
        return ImageDraw.Draw(self._img)


class Content(ABC):
    def __init__(self, xy=(0, 0), value=None):
        self.xy = xy
        self.static = True if value else False
        self.value = value

    def update_value(self, new_value) -> bool:
        if new_value != self.value:
            self.value = new_value
            return True
        return False

    @abstractmethod
    def paint_at_box(self, box: Tuple[int, int] = DEFAULT_CONTAINER) -> Canvas:
        """Renders self at provided canvas (typically at parent's canvas)"""
        canvas = Canvas(box)
        return canvas


class Container(ABC):
    def __init__(self, xy, size, fill, radius, content={}):
        self.xy = xy
        self.fill = fill
        self.radius = radius
        self.content: Dict[str, Content] = content
        self.size = size
        self._canvas: Canvas = Canvas(size)

    def paint_content(self):
        """Widget renders itself if it is changed"""
        self._canvas.fill(self.fill, self.radius)
        for child in self.content.values():
            self._canvas.paste(child.paint_at_box(self.size), child.xy)

    @property
    def image(self):
        return self._canvas()


class Text(Content):
    def __init__(self, value=None, **kwargs):
        super().__init__(value=value)
        self._args = kwargs

    def paint_at_box(self, box=DEFAULT_CONTAINER):
        canvas = super().paint_at_box(box)
        self._args["text"] = self.value
        canvas.draw.multiline_text(**self._args)
        return canvas()


class ImageView(Content):
    def __init__(self, x=0, y=0, value=None):
        super().__init__(value=value)
        self._position = (x, y)

    def paint_at_box(self, box=DEFAULT_CONTAINER) -> Canvas:
        canvas = super().paint_at_box(box)
        canvas.paste_from_url(self.value, self._position)
        return canvas()


class Rect(Content):
    def __init__(self, xy=(0, 0, 0, 0),
                 fill=Colors.panel_bg, radius=DEFAULT_RADIUS):
        super().__init__()
        self._args = {
            "xy": xy,
            "radius": radius,
            "fill": fill
        }

    def paint_at_box(self, box=DEFAULT_CONTAINER):
        canvas = super().paint_at_box(box)
        canvas.draw.rounded_rectangle(**self._args)
        return canvas()


class Widget(Container):
    def __init__(self, content={},
                 size=DEFAULT_CONTAINER, xy=(0, 0),
                 fill=(0, 0, 0, 0), radius=0):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(
            content=content,
            xy=xy, size=size, fill=fill, radius=radius)
        self._state = {
            key: "" for key in self.content.keys()
        }
        self._name = ""
        self.dirty = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: dict):
        for k, v in new_state.items():
            if not (k in self._state.keys()):
                raise ValueError(
                    f"Unknown key <{k}>",
                )
            if not isinstance(v, str):
                raise TypeError(
                    f"Expected <str>. Got <{type(v).__name__}>",
                )
            if self._state[k] != new_state[k]:
                self._state[k] = v
                self.dirty = True

    def update(self):
        for key, item in self.content.items():
            if not item.static:
                item.update_value(self._state[key])
        self.paint_content()


"""
class WeekProgress(Content):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self._value = "0"

    def render(self):
        numb = int(self._value)
        self._canvas.clear()
        for i in range(7):
            if numb >= (i + 1):
                fill = Colors.DEFAULT
            else:
                fill = (0, 0, 0, 0)
            self._canvas.draw.circle(
                xy=(self.x + 10 + i * 36, self.y + 10),
                radius=10,
                fill=fill,
                outline=Colors.DEFAULT,
                width=2)
"""
