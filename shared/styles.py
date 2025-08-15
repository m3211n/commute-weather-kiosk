from PIL import ImageFont


def get_font(path, size):
    return ImageFont.truetype(path, size)


FONT_PATHS = {
    "black": "./shared/fonts/MuseoModerno-Black.ttf",
    "bold": "./shared/fonts/MuseoModerno-Bold.ttf",
    "regular": "./shared/fonts/MuseoModerno-Regular.ttf",
    "mono": "./shared/fonts/RobotoMono-Regular.ttf"
}


class Fonts:
    """Font presets for the UI."""
    VALUE = get_font(FONT_PATHS["regular"], 86)
    LABEL_SMALL = get_font(FONT_PATHS["regular"], 40)
    LABEL_XSMALL = get_font(FONT_PATHS["regular"], 32)
    LABEL_LARGE = get_font(FONT_PATHS["regular"], 63)
    WEATHER_TODAY = get_font(FONT_PATHS["regular"], 137)
    CLOCK = get_font(FONT_PATHS["bold"], 211)
    DEPARTURES = get_font(FONT_PATHS["bold"], 40)
    STATUS = get_font(FONT_PATHS["mono"], 20)

    @staticmethod
    def custom(name: str, size: int):
        """Get a custom font by name and size."""
        return get_font(FONT_PATHS[name], size)


class Colors:
    """Color palette for the UI."""
    PANEL_BG = (16, 16, 16, 255)
    TITLE = (255, 255, 255, 88)
    DEPARTURES = (216, 216, 0, 255)
    DEFAULT = (255, 255, 255, 255)
    SECONDARY = (255, 255, 255, 150)
    NONE = (0, 0, 0, 0)
