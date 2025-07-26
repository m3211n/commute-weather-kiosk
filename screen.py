from PIL import Image
import asyncio
import numpy as np

WIDTH, HEIGHT = 1920, 1080

def rgb888_to_rgb565_numpy(image):
    arr = np.array(image, dtype=np.uint8)
    r = arr[:, :, 0].astype(np.uint16)
    g = arr[:, :, 1].astype(np.uint16)
    b = arr[:, :, 2].astype(np.uint16)
    rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    return rgb565.astype('<u2').tobytes()

class Screen(Image.Image):
    def __new__(cls):
        obj = Image.new("RGB", (WIDTH, HEIGHT), "black")
        obj.__class__ = cls
        return obj

    def compose(self, sections):
        for section in sections:
            section.paste_to(self)
        return self

    async def output(self):
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, self)
        with open("/dev/fb0", "wb") as f:
            f.write(buf)