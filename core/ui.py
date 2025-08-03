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
        widget_dirty = False
        if self.timer.done():
            for child in self.children:
                child_dirty = child.update()
                widget_dirty = widget_dirty or child_dirty
        return widget_dirty

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
        new_text = self._callback()
        if self.text != new_text:
            self.text = new_text
            return True
        return False


class ImageWidget(Widget):
    def __init__(
            self, url,
            position=(0, 0),
            update_callback=None,
            interval=1
            ):
        self.url = url
        self.image_cache = Image.open(self.url)
        super().__init__(
            position=position,
            update_callback=update_callback,
            interval=interval
        )

    async def render(self):
        return self.image_cache

    def update(self):
        new_url = self._callback()
        if new_url and (len(new_url) > 0) and (self.url != new_url):
            self.url = new_url
            self.image_cache = Image.open(self.url)
            logging.debug("Loaded new image")
            return True
        return False


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
