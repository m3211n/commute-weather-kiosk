from PIL import Image
import numpy as np
import asyncio
import time

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200

def rgb888_to_rgb565_numpy(image):
    arr = np.asarray(image.convert("RGB"))  # ensures RGB mode, shape (H, W, 3), dtype=uint8
    arr16 = arr.astype(np.uint16)           # single cast for all channels

    r = (arr16[:, :, 0] & 0xF8) << 8         # 5 bits
    g = (arr16[:, :, 1] & 0xFC) << 3         # 6 bits
    b = (arr16[:, :, 2] & 0xF8) >> 3         # 5 bits

    rgb565 = r | g | b
    return rgb565.astype('<u2').tobytes()   # little-endian for /dev/fb0


class Screen:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bgcolor=(0, 0, 0)):
        self.width = width
        self.height = height
        self.fb = None
        self.widgets = {}
        self._bgcolor = bgcolor

    def __enter__(self):
        self.fb = open("/dev/fb0", "r+b", buffering=0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fb:
            self.fb.close()

    def add(self, widgets):
        """Add a widget-like object with .x, .y, .get_image() and a name to refer to it"""
        for widget in widgets:
            self.widgets[widget.name] = widget

    async def refresh_all(self, bulk=False):
        """Render and draw all layers to the framebuffer"""
        for widget in self.widgets.values():
            image = await asyncio.to_thread(widget.get_image)
            write = self.write_at if not bulk else self.write_at_bulk
            print("--- Benchmarking:")
            start = time.time()
            await write(widget.x, widget.y, image)
            end = time.time() - start
            print(f"--- Done in {end} s.")

    async def write_at(self, x, y, image):
        print("Write_at() -- seek() + write rows")
        img_w, img_h = image.size
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, image)

        row_size = self.width
        fb_offset = (y * row_size + x) * 2
        for row in range(img_h):
            offset = fb_offset + row * row_size * 2
            start = row * img_w * 2
            end = start + img_w * 2
            self.fb.seek(offset)
            self.fb.write(buf[start:end])

    async def write_at_bulk(self, x, y, image):
        """Compose the entire framebuffer in memory and write at once."""
        print("Write_at_bulk() -- PIL.Image.paste() + write full buffer")
        # Create a full-size image with the current background
        fb_img = Image.new("RGB", (self.width, self.height), self._bgcolor)
        fb_img.paste(image, (x, y))
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, fb_img)
        self.fb.seek(0)
        self.fb.write(buf)

    async def clear(self):
        image = Image.new("RGB", (self.width, self.height), self._bgcolor)
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, image)
        self.fb.seek(0)
        self.fb.write(buf)        
