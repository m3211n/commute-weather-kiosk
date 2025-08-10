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
    LABEL_LARGE = get_font(FONT_PATHS["regular"], 63)
    WEATHER_TODAY = get_font(FONT_PATHS["regular"], 211)
    CLOCK = get_font(FONT_PATHS["bold"], 211)
    STATUS = get_font(FONT_PATHS["mono"], 20)

    @staticmethod
    def custom(name: str, size: int):
        """Get a custom font by name and size."""
        return get_font(FONT_PATHS[name], size)


class Colors:
    """Color palette for the UI."""
    PANEL_BG = (16, 16, 16, 255)
    TITLE = (255, 255, 255, 88)
    DEPARTURE_TIMES = (216, 216, 0)
    DEFAULT = (255, 255, 255, 255)
    SECONDARY = (255, 255, 255, 200)
    NONE = (0, 0, 0, 0)
