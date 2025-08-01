from typing import List
from core.data_sources import Tools
from PIL import Image, ImageDraw
from shared.styles import Fonts, Colors
import logging


class Container:
    def __init__(self, xy=(0, 0), size=(100, 100)):
        self.xy = xy
        self.size = size
        self.image = Image.new("RGB", self.size)
        self.draw_context = ImageDraw.Draw(self.image)

    def _clear(self):
        self.image.paste(Colors.NONE, self.box)

    @property
    def box(self):
        return (*self.xy, self.xy[0] + self.size[0], self.xy[1] + self.size[1])


class DynamicContainer(Container):
    def __init__(self, xy, size, timeout=1):
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

    async def maybe_render(self) -> bool:
        if await self.update_children():
            await self.render()
            return True
        return False


class DynamicText:
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


class Label(DynamicText):
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
    def __init__(self, xy, size, fill=Colors.PANEL_BG, radius=24, timeout=1):
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


class ImageWidget(DynamicContainer):
    def __init__(self, xy, size, img_url, timeout=1):
        super().__init__(xy, size, timeout)
        self.bg = Image.open(img_url)

    def _clear(self):
        super()._clear()
        self.image.paste(self.bg)
