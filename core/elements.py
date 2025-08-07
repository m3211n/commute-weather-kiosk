from core.styles import Fonts, Colors
from PIL import Image, ImageDraw


DEFAULT_SIZE = 100
DEFAULT_RADIUS = 24


class Widget:
    def __init__(
            self, xy=(0, 0), size=(DEFAULT_SIZE, DEFAULT_SIZE),
            bg_color=Colors.PANEL_BG, bg_img=None
            ):
        """Initializes widget. If image is provided, then background color
        is ignored."""

        self.xy = xy
        self.size = size
        self.bg: Image.Image = (
            self._load_img(bg_img) if bg_img else self._draw_r_rect(bg_color)
        )
        self.children = []
        self._image: Image.Image = None

    def _draw_r_rect(self, color) -> Image.Image:
        self._image = Image.new("RGBA", self.size)
        ImageDraw.Draw(self._image).rounded_rectangle(
            self.xy, DEFAULT_RADIUS, fill=color)
        return self._image

    def _load_img(self, url) -> Image.Image:
        self._image = Image.open(url)
        return self._image

    def update(self, data):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


class TextLabel(Widget):
    def __init__(self, xy, fill=Colors.DEFAULT, font=Fonts.VALUE, anchor="lt"):
        super().__init__(xy=xy)
        self.fill = fill
        self.font = font
        self.anchor = anchor
        self.text = ""
        self._image = None

    def update(self, text: str):
        """
        Changes the text of the label if new value is different from the
        current one. Returns True if text was updated and False if it wasn't.
        """

        if not text == self.text:
            self.text = text
            bbox = self.font.getbbox(self.text)
            self.size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
            return True
        return False

    def render(self):
        """Renders the image based on the current text unconditionally."""
        self._image = Image.new("RGBA", self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self._image)
        draw.text(
            (0, 0), self.text, font=self.font, fill=self.fill,
            anchor=self.anchor)
        return self._image


class Icon(Widget):
    def __init__(self, url, xy=(0, 0)):
        super().__init__(xy=xy)
        self._image: Image.Image = self._load_img(url)

    def _load_img(self, url) -> Image.Image:
        self._image = Image.open(url)

    def render(self) -> Image.Image:
        return self._image
