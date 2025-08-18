from PIL import ImageFont


def get_font(path, size):
    return ImageFont.truetype(path, size)


FONT_PATHS = {
    "bold": "./shared/fonts/Geist-Bold.ttf",
    "regular": "./shared/fonts/Geist-Regular.ttf",
    "light": "./shared/fonts/Geist-Light.ttf",
    "mono": "./shared/fonts/RobotoMono-Regular.ttf",
    "icon": "./shared/fonts/weathericons-regular-webfont.ttf"
}


class Fonts:
    """Font presets for the UI."""

    ICON_XSMALL = get_font(FONT_PATHS["icon"], 36)

    H1 = get_font(FONT_PATHS["light"], 160)
    H2 = get_font(FONT_PATHS["light"], 40)
    H3 = get_font(FONT_PATHS["light"], 32)
    H4 = get_font(FONT_PATHS["light"], 28)

    D1 = get_font(FONT_PATHS["bold"], 240)
    D2 = get_font(FONT_PATHS["bold"], 100)
    D3 = get_font(FONT_PATHS["bold"], 63)
    D4 = get_font(FONT_PATHS["bold"], 40)

    STATUS = get_font(FONT_PATHS["mono"], 20)

    @staticmethod
    def font(name: str, size: int):
        """Get a custom font by name and size."""
        return get_font(FONT_PATHS[name], size)


class Colors:
    """Color palette for the UI."""
    PANEL_BG = (16, 16, 16, 255)
    TITLE = (255, 255, 255, 88)
    DEPARTURES = (216, 216, 0, 255)
    DEFAULT = (255, 255, 255, 255)
    SECONDARY = (255, 255, 255, 10)
    NONE = (0, 0, 0, 0)
