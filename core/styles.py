from dataclasses import dataclass
from typing import Tuple as _Tuple
from PIL import ImageFont


RGB = _Tuple[int, int, int]
RGBA = _Tuple[int, int, int, int]


class TextStyle(dict):
    def __init__(self, font_path: str = "", size=16,
                 fill=(255, 255, 255, 255), anchor="la", **kwargs):
        self["font"] = ImageFont.truetype(font_path, size)
        self["fill"] = fill
        self["anchor"] = anchor
        for k, v in kwargs.items():
            self[k] = v

    def copy(self, **overrides):
        new = dict(self)
        new.update(overrides)
        return TextStyle._from_dict(new)

    @classmethod
    def _from_dict(cls, d: dict):
        obj = cls.__new__(cls)
        super(TextStyle, obj).__init__(d)
        return obj


@dataclass(frozen=True)
class Fonts:
    bold: str = "./assets/fonts/Geist-Bold.ttf"
    regular: str = "./assets/fonts/Geist-Regular.ttf"
    light: str = "./assets/fonts/Geist-Light.ttf"
    mono: str = "./assets/fonts/RobotoMono-Regular.ttf"
    icon: str = "./assets/fonts/weathericons-regular-webfont.ttf"


@dataclass(frozen=True)
class Colors:
    """Color palette for the UI."""
    panel_bg: RGBA = (16, 16, 16, 255)
    default: RGB = (255, 255, 255)
    secondary: RGBA = (255, 255, 255, 192)
    tetriary: RGBA = (255, 255, 255, 96)
    highlight: RGB = (216, 216, 0)
    none: RGBA = (0, 0, 0, 0)
    black: RGB = (0, 0, 0)


@dataclass(frozen=True)
class TextStyles:

    # Labels
    status = TextStyle(Fonts.mono, 22, Colors.tetriary, "lm")
    status_rt = status.copy(anchor="rm")
    time = TextStyle(Fonts.bold, 200, anchor="ma")
    date = TextStyle(Fonts.bold, 40, anchor="ma")
    temperature = TextStyle(Fonts.regular, 200)
    weather_cond = TextStyle(Fonts.regular, 40)
    icon = TextStyle(Fonts.icon, 36)
    details = TextStyle(Fonts.regular, 32)
    transport_title = details.copy(fill=Colors.tetriary)

    # Paragraphs
    line_codes = TextStyle(
        font_path=Fonts.regular,
        size=48,
        spacing=18,
        anchor=None
    )
    destinations = TextStyle(
        font_path=Fonts.regular,
        size=48,
        fill=Colors.secondary,
        spacing=18,
        anchor=None
    )
    departures = TextStyle(
        font_path=Fonts.bold,
        size=48,
        fill=Colors.highlight,
        spacing=18,
        features=["tnum"],
        align="right",
        anchor="ra"
    )
    weather_icons = icon.copy(spacing=31, align="center", anchor=None)
    temps = details.copy(
        spacing=38,
        anchor=None
    )
    hours = details.copy(
        fill=Colors.secondary,
        spacing=38,
        anchor=None,
        features=["tnum"]
    )
