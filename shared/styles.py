from PIL import ImageFont


def font(name: str, size: int):
    FONT_PATHS = {
        "bold": "./shared/fonts/Geist-Bold.ttf",
        "regular": "./shared/fonts/Geist-Regular.ttf",
        "light": "./shared/fonts/Geist-Light.ttf",
        "mono": "./shared/fonts/RobotoMono-Regular.ttf",
        "icon": "./shared/fonts/weathericons-regular-webfont.ttf"
    }
    path = FONT_PATHS[name]
    return ImageFont.truetype(path, size)


class Colors:
    """Color palette for the UI."""
    PANEL_BG = (16, 16, 16, 255)
    TETRIARY = (255, 255, 255, 88)
    DEPARTURES = (216, 216, 0, 255)
    DEFAULT = (255, 255, 255, 255)
    SECONDARY = (255, 255, 255, 192)
    NONE = (0, 0, 0, 0)
