from PIL import Image
import asyncio
import os
from datetime import datetime
import numpy as np

WIDTH, HEIGHT = 1920, 1200

def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

class Screen:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

    def compose(self, sections):
        image = Image.new("RGB", (self.width, self.height), "black")
        for section in sections:
            section.paste_to(image)
        return image

    async def output(self, image, fb=True):
        task = self._write_to_fb if fb else self._write_to_img
        await asyncio.to_thread(task, image)

    # def _write_to_fb(self, image):
    #     pixels = image.load()
    #     with open("/dev/fb0", "wb") as f:
    #         for y in range(self.height):
    #             for x in range(self.width):
    #                 r, g, b = pixels[x, y]
    #                 rgb565 = rgb888_to_rgb565(r, g, b)
    #                 f.write(struct.pack("<H", rgb565))

    def _write_to_fb(self, image):
        arr = np.array(image, dtype=np.uint8)
        r = arr[:, :, 0].astype(np.uint16)
        g = arr[:, :, 1].astype(np.uint16)
        b = arr[:, :, 2].astype(np.uint16)

        # RGB888 → RGB565 (5-6-5 bits)
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

        # Convert to little-endian byte order
        buf = rgb565.astype('<u2').tobytes()

        with open("/dev/fb0", "wb") as f:
            f.write(buf)

    def _write_to_img(self, image):
        try:
            os.mkdir("__preview")
        except FileExistsError:
            pass
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"__preview/{timestamp}.jpg"
        image.save(filename, "JPEG")