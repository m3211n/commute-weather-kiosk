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

class Screen:
    def __init__(self, width=1920, height=1080):
        self.image = Image.new("RGB", (width, height), "black")

    def compose(self, sections):
        for section in sections:
            section.paste_to(self.image)
        return self.image

    async def output(self):
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, self.image)
        with open("/dev/fb0", "wb") as f:
            f.write(buf)