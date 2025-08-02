from typing import List
from core.tools import IntervalLoop
from core.data_sources import Tools
from PIL import Image, ImageDraw
from core.styles import Fonts, Colors
import logging


class Widget:
    def __init__(
            self, position=(0, 0),
            size=(100, 100),
            fill=Colors.PANEL_BG,
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
            children_img.paste(child_img, child.xy, mask=child_img.split()[3])
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


class Container:
    def __init__(self, xy=(0, 0), size=(100, 100)):
        self.xy = xy
        self.size = size
        self._image = Image.new("RGBA", self.size)
        self.draw_context = ImageDraw.Draw(self._image)

    def _clear(self):
        self._image.paste(Colors.NONE, self.box)

    @property
    def box(self):
        return (*self.xy, self.xy[0] + self.size[0], self.xy[1] + self.size[1])

    @property
    async def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image


class DynamicContainer(Container):
    def __init__(self, xy, size, timeout):
        super().__init__(xy, size)
        self._timeout = timeout
        self._next_update = Tools.time()
        self.children: List[Container] = []

    def _update_timer(self):
        if self._next_update < Tools.time():
            target = self.__class__.__name__
            logging.debug(" >>> Update triggered from: %s", target)
            self._next_update = Tools.time() + self._timeout
            logging.debug(" *** Next update is in: %d", self._timeout)
            return True
        return False

    async def update_children(self) -> bool:
        if self._update_timer():
            for item in self.children:
                item.update()
            return True
        return False

    async def render(self) -> bool:
        self._clear()
        for child in self.children:
            child.draw_context = self.draw_context
            try:
                await child.render()
            except ValueError as e:
                raise e

    async def maybe_update(self) -> bool:
        if await self.update_children():
            await self.render()
            return True
        return False


class DynamicTextLabel:
    def __init__(self, xy, size, callback=None):
        self.xy = xy
        self.size = size
        self.text = ""
        self.do_update = callback if callback else self._callback_dummy
        self.draw_context = None

    def _callback_dummy(self) -> str:
        return "Just a label"

    def update(self):
        self.text = self.do_update()


class Label(DynamicTextLabel):
    """Generic label class.
    Uses the same attributes as PIL.ImageDraw.Draw.text"""

    def __init__(self, callback=None, xy=(0, 0), size=(0, 0),
                 fill=Colors.DEFAULT, font=Fonts.VALUE, anchor="la"):
        super().__init__(xy, size, callback)
        self.fill = fill
        self.font = font
        self.anchor = anchor

    async def render(self):
        if len(self.text) == 0:
            raise Warning("Attempt to render empty string skipped.")
        else:
            try:
                self.draw_context.text(**self.__dict__)
            except AttributeError as e:
                raise e


class ColorWidget(DynamicContainer):
    """Generic widget class"""
    def __init__(self, xy, size, radius=24, timeout=1, fill=Colors.PANEL_BG):
        super().__init__(xy, size, timeout)
        self.fill = fill
        self.radius = radius

    def _clear(self):
        super()._clear()
        self.draw_context.rounded_rectangle(
            [(0, 0), self.size],
            radius=self.radius,
            fill=self.fill
        )


class DynamicImage(DynamicContainer):
    def __init__(self, xy, size, img_url, timeout):
        super().__init__(xy, size, timeout)
        self.bg = Image.open(img_url)

    def _clear(self):
        super()._clear()
        self._image.paste(self.bg)
