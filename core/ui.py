from typing import List
from core.tools import IntervalLoop
from PIL import Image, ImageDraw
from core.styles import Fonts, Colors
import logging


class Widget:
    def __init__(
            self,
            update_callback=None,
            position=(0, 0),
            size=(100, 100),
            fill=(0, 0, 0, 255),
            interval=1):
        self.xy = position
        self.size = size
        self.fill = fill
        self.children: List[Widget] = []
        self._callback = update_callback if update_callback else self._dummy
        self.timer = IntervalLoop(interval=interval)

    def _dummy(self):
        logging.debug("Default update method triggered")
        return None

    def update(self):
        self._callback()

    async def maybe_update(self):
        if self.timer.done():
            for child in self.children:
                child.update() if hasattr(child, "update") else None
            return True
        return False

    def draw(self, img):
        pass

    async def render(self) -> Image.Image:
        img = Image.new("RGBA", self.size, color=self.fill)
        children_img = Image.new("RGBA", self.size, color=(0, 0, 0, 0))
        for child in self.children:
            child.draw(children_img)
            child_img: Image.Image = await child.render()
            img.paste(child_img, child.xy, mask=child_img.split()[3])
        # Merging image with children to background layer
        img.paste(children_img, (0, 0), mask=children_img.split()[3])
        return img

    @property
    async def image(self):
        return await self.render()


class DrawGroup(Widget):
    def __init__(
            self, position=(0, 0),
            size=(100, 100),
            fill=Colors.NONE,
            children: List[Widget] = []
            ):
        super().__init__(
            position=position,
            size=size,
            fill=fill
        )
        self.children = children

    def update(self):
        for child in self.children:
            child.update() if hasattr(child, "update") else None

    async def render(self):
        img = Image.new("RGBA", size=self.size, color=self.fill)
        for child in self.children:
            child.draw(img)
        return img


class TextWidget(Widget):
    def __init__(
            self, position=(0, 0),
            font=Fonts.VALUE,
            color=Colors.DEFAULT,
            fill=Colors.NONE,
            anchor="lt",
            update_callback=None,
            interval=1
            ):
        self.font = font
        self._callback = update_callback
        self.text = self._callback() if self._callback else ""
        bbox = self.font.getbbox(self.text) if self.text else (0, 0, 100, 20)
        size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        super().__init__(
            update_callback=update_callback,
            position=position,
            size=size,
            interval=interval,
            fill=fill
        )
        self.color = color
        self.anchor = anchor

    def draw(self, img):
        logging.debug("Drawing text %s", self.text)
        if self.text and len(self.text) > 0:
            ImageDraw.Draw(img).text(
                xy=self.xy,
                text=self.text,
                fill=self.color,
                font=self.font,
                anchor=self.anchor
            )
        else:
            logging.debug("Got None instead of text!")
            # raise ValueError("Got None instead of text!")

    def update(self):
        old_text = self.text
        self.text = self._callback() if self._callback else ""
        # Only recalculate size if text changed
        if old_text != self.text:
            if self.text:
                bbox = self.font.getbbox(self.text)
            else:
                bbox = (0, 0, 100, 20)
            self.size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        logging.debug(
            "Text label updated to: %s",
            self.text
        )


class ImageWidget(Widget):
    _image_cache = {}  # Class-level cache for loaded images

    def __init__(
            self, url,
            position=(0, 0),
            update_callback=None,
            interval=0
            ):
        self.url = url
        # Pre-load and cache the image
        if url not in ImageWidget._image_cache:
            ImageWidget._image_cache[url] = Image.open(url)
        super().__init__(
            position=position,
            update_callback=update_callback,
            interval=interval
        )

    async def render(self):
        return ImageWidget._image_cache[self.url].copy()


class ColorFill(Widget):
    def __init__(self, parent: Widget, color=Colors.PANEL_BG, radius=24):
        super().__init__(size=parent.size)
        self.radius = radius
        self.fill = color

    async def render(self):
        img = Image.new("RGBA", self.size, (0, 0, 0, 0))
        ImageDraw.Draw(img).rounded_rectangle(
            (0, 0, *self.size),
            radius=self.radius,
            fill=self.fill
        )
        return img
