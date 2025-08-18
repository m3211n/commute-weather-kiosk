from PIL import Image, ImageDraw
import numpy as np


async def convert(image: Image.Image):
    """Convert image from RGB888 to RGB565
    for /dev/fb0 on Pi Zero 2W"""
    # Flatten RGBA image
    flattened_image = Image.new("RGBA", image.size, (0, 0, 0, 255))
    flattened_image.paste(image, mask=image.split()[3])
    arr = np.asarray(flattened_image)
    arr16 = arr.astype(np.uint16)
    r = (arr16[:, :, 0] & 0xF8) << 8         # 5 bits
    g = (arr16[:, :, 1] & 0xFC) << 3         # 6 bits
    b = (arr16[:, :, 2] & 0xF8) >> 3         # 5 bits
    rgb565 = r | g | b
    # little-endian for /dev/fb0
    return rgb565.astype('<u2').tobytes()


def clear(block, mode=0):
    """Returns block of transparent pixels (mode=0), black pixels (mode=1) or
    zeros (mode=2). Default mode is 0"""
    match mode:
        case 0:
            img = Image.new("RGBA", block)
        case 1:
            img = Image.new("RGB", block)
        case _:
            img = np.zeros(block, dtype="<u2")
    return img


def clear_bytes(block):
    """Returns block of transparent pixels (mode=0), black pixels (mode=1) or
    zeros (mode=2). Default mode is 0"""
    return np.zeros(block, dtype="<u2")


class Canvas:
    def __init__(self, size, mode="RGBA"):
        self._mode = mode
        self._img = Image.new(mode=self._mode, size=size)

    def __call__(self) -> Image.Image:
        return self._img

    def clear(self) -> "Canvas":
        size = self._img.size
        self._img = Image.new(mode=self._mode, size=size)
        return self

    def fill(self, color=(0, 0, 0, 0), radius=0) -> "Canvas":
        self.draw.rounded_rectangle(
            [0, 0, *self._img.size],
            radius=radius,
            fill=color
        )
        return self

    def paste(self, img: Image.Image, xy=(0, 0)):
        mask = img.split()[3]
        self._img.paste(img, xy, mask=mask)

    def copy(self) -> "Canvas":
        copy = Canvas(self._img.size, self._mode)
        copy._img = self._img.copy()
        return copy

    def load(self, url, xy=(0, 0)) -> "Canvas":
        img = Image.open(url)
        self._img.paste(img, xy)
        return self

    @property
    def draw(self):
        return ImageDraw.Draw(self._img)
