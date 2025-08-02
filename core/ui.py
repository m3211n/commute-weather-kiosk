from typing import List
from core.tools import IntervalLoop
from PIL import Image, ImageDraw
from core.styles import Fonts, Colors
import logging


class Widget:
    def __init__(
            self, position=(0, 0),
            size=(100, 100),
            fill=(0, 0, 0, 255),
            update_callback=None,
            interval=1):
        self.xy = position
        self.size = size
        self.fill = fill
        self.children: List[Widget] = []
        self.update = update_callback if update_callback else self._dummy
        self.timer = IntervalLoop(interval=interval)

    def _dummy(self):
        logging.debug("Default update method triggered")
        return None

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
        self._callback = update_callback
        self.font = font
        self.text = self._callback()
        bbox = self.font.getbbox(self.text)
        size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        super().__init__(
            position=position,
            size=size,
            interval=interval,
            fill=fill
        )
        self.color = color
        self.anchor = anchor

    def draw(self, img):
        ImageDraw.Draw(img).text(
            xy=self.xy,
            text=self.text,
            fill=self.color,
            font=self.font,
            anchor=self.anchor
        )

    def update(self):
        self.text = self._callback()


class ImageWidget(Widget):
    def __init__(
            self, url,
            position=(0, 0),
            update_callback=None,
            interval=0
            ):
        self.url = url
        super().__init__(
            position=position,
            update_callback=update_callback,
            interval=interval
        )

    async def render(self):
        return Image.open(self.url)


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
