from widgets.data_sources import Tools
from PIL import Image, ImageDraw
from shared.styles import Fonts, Colors


class Label:
    """Generic label class.
    Uses the same attributes as PIL.ImageDraw.Draw.text"""

    def __init__(self, xy=(0, 0), text="Label", fill=Colors.DEFAULT,
                 font=Fonts.VALUE, anchor="la"):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font = font
        self.anchor = anchor

    async def render_at(self, image):
        if len(self.text) == 0:
            raise Warning("Attempt to render empty string skipped.")
        else:
            _draw_context = ImageDraw.Draw(image)
            try:
                _draw_context.text(**self.__dict__)
            except AttributeError as e:
                raise e


class Widget:
    """Generic widget class"""
    def __init__(
            self,
            position=(0, 0),
            size=(100, 100),
            bgcolor=Colors.PANEL_BG,
            radius=16,
            timeout=1,
            ):
        self.timeout = timeout
        self._last_update = Tools.time()
        self.position = position
        self.size = size
        self.bgcolor = bgcolor
        self.radius = radius
        self.image = Image.new("RGB", self.size)
        self._draw_context = ImageDraw.Draw(self.image)

    def _update_timeout(self):
        if self._last_update < Tools.time():
            self._last_update = Tools.time() + self.timeout
            return True
        return False

    def _clear(self):
        self._draw_context.rounded_rectangle(
            [(0, 0), self.size],
            radius=self.radius,
            fill=self.bgcolor
        )

    async def update_content(self) -> bool:
        return False

    async def maybe_render(self) -> bool:
        if await self.update_content():
            await self.render()
            return True
        return False

    async def render(self) -> bool:
        self._clear()
