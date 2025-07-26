from PIL import Image
import struct
import asyncio
import os
from datetime import datetime

WIDTH, HEIGHT = 1920, 1080

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

    def _write_to_fb(self, image):
        pixels = image.load()
        with open("/dev/fb0", "wb") as f:
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = pixels[x, y]
                    rgb565 = rgb888_to_rgb565(r, g, b)
                    f.write(struct.pack("<H", rgb565))

    def _write_to_img(self, image):
        try:
            os.mkdir("__preview")
        except FileExistsError:
            pass
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"__preview/{timestamp}.jpg"
        image.save(filename, "JPEG")