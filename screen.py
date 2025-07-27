from PIL import Image
import numpy as np
import asyncio

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200

def rgb888_to_rgb565_numpy(image):
    arr = np.array(image, dtype=np.uint8)
    r = arr[:, :, 0].astype(np.uint16)
    g = arr[:, :, 1].astype(np.uint16)
    b = arr[:, :, 2].astype(np.uint16)
    rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    return rgb565.astype('<u2').tobytes()


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

    def add(self, widget):
        """Add a widget-like object with .x, .y, .get_image() and a name to refer to it"""
        self.widgets[widget.name] = widget
        return len(self.widgets) - 1

    async def refresh_all(self):
        """Render and draw all layers to the framebuffer"""
        for widget in self.widgets.values():
            image = await asyncio.to_thread(widget.get_image)
            await self.write_at(widget.x, widget.y, image)

    async def write_at(self, x, y, image):
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

    async def clear(self):
        image = Image.new("RGB", (self.width, self.height), self._bgcolor)
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, image)
        self.fb.seek(0)
        self.fb.write(buf)        
