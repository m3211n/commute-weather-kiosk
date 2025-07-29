from PIL import ImageFont


def get_font(path, size):
    return ImageFont.truetype(path, size)


FONT_PATHS = {
    "dejavu_sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "dejavu_mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}


class Fonts:
    """Font presets for the UI."""
    VALUE = get_font(FONT_PATHS["dejavu_sans"], 80)
    TITLE = get_font(FONT_PATHS["dejavu_mono"], 40)
    WEATHER_TODAY = get_font(FONT_PATHS["dejavu_sans"], 120)
    CLOCK = get_font(FONT_PATHS["dejavu_sans"], 240)
    STATUS = get_font(FONT_PATHS["dejavu_mono"], 20)

    @staticmethod
    def custom(name: str, size: int):
        """Get a custom font by name and size."""
        return get_font(FONT_PATHS[name], size)


class Colors:
    """Color palette for the UI."""
    PANEL_BG = (32, 32, 32)
    TITLE = (88, 88, 88)
    DEPARTURE_TIMES = (216, 216, 0)
    DEFAULT = (216, 216, 216)
    SECONDARY = (160, 160, 160)
    NONE = (0, 0, 0)
