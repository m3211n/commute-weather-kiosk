from PIL import Image
import numpy as np


async def rgb888_to_rgb565_numpy(image: Image.Image):
    """Convert image from RGB888 to RGB565
    for /dev/fb0 on Pi Zero 2W"""
    arr = np.asarray(image)
    arr16 = arr.astype(np.uint16)
    r = (arr16[:, :, 0] & 0xF8) << 8         # 5 bits
    g = (arr16[:, :, 1] & 0xFC) << 3         # 6 bits
    b = (arr16[:, :, 2] & 0xF8) >> 3         # 5 bits
    rgb565 = r | g | b
    # little-endian for /dev/fb0
    return rgb565.astype('<u2').tobytes()


def clear(block):
    return np.zeros(block, dtype="<u2")


def clear_rgb(block) -> Image:
    return Image.new("RGB", block)
