from typing import List
from core.data_sources import Tools
from PIL import Image, ImageDraw
from shared.styles import Fonts, Colors
import logging


class Content:
    def __init__(self):
        self.render_context = None
        self.value = None

    def render(self):
        pass


class Label(Content):
    """Generic label class.
    Uses the same attributes as PIL.ImageDraw.Draw.text"""

    def __init__(self, update_callback=None, xy=(0, 0), fill=Colors.DEFAULT,
                 font=Fonts.VALUE, anchor="la"):
        self.xy = xy
        self.text = self._update_callback_placeholder()
        self.fill = fill
        self.font = font
        self.anchor = anchor
        if update_callback:
            self.update_callback = update_callback
        else:
            self.update_callback = self._update_callback_placeholder

    def _update_callback_placeholder(self) -> str:
        return "Just a label"

    def update(self):
        self.text = self.update_callback()

    async def render(self):
        if len(self.text) == 0:
            raise Warning("Attempt to render empty string skipped.")
        else:
            try:
                self.render_context.text(**self.__dict__)
            except AttributeError as e:
                raise e


class Widget:
    """Generic widget class"""
    def __init__(
            self,
            position=(0, 0),
            size=(100, 100),
            bgcolor=Colors.PANEL_BG,
            image_url="",
            radius=24,
            timeout=1,
            ):
        self.timeout = timeout
        self._last_update = Tools.time()
        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.radius = radius
        self.image = Image.new("RGB", self.size)
        self.bg = self._get_background(image_url)
        self.render_context = ImageDraw.Draw(self.image)
        self.content: List[Content] = []

    def _get_background(self, url=""):
        if len(url) > 0:
            bg = Image.open(url)
            logging.debug(f"--Opened image from URL <{url}>")
        else:
            bg = Image.new("RGB", self.size)
            tmp_context = ImageDraw.Draw(bg)
            tmp_context.rounded_rectangle(
                [(0, 0), self.size],
                radius=self.radius,
                fill=self.bgcolor
            )
        return bg

    def _update_timeout(self):
        if self._last_update < Tools.time():
            self._last_update = Tools.time() + self.timeout
            return True
        return False

    def _clear(self):
        self.image.paste(self.bg)

    async def update_content(self) -> bool:
        if self._update_timeout():
            for item in self.content:
                item.update()
            return True
        return False

    async def maybe_render(self) -> bool:
        if await self.update_content():
            await self.render()
            return True
        return False

    async def render(self) -> bool:
        self._clear()
        logging.debug(
            f"Rendering {len(self.content)} items."
        )
        for item in self.content:
            logging.debug(f"Rendering {item.__class__.__name__}")
            item.render_context = self.render_context
            try:
                await item.render()
            except ValueError as e:
                raise e
