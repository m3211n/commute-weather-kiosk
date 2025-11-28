import logging
import time

from typing import Dict
from core.render import clear, clear_bytes, Image
from core.ui import Widget

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
BYTES_PER_PIXEL = 2
FB_PATH = "/dev/fb0"
BG_COLOR = (0, 0, 0)


class Display:
    """ Generic screen class to dump buffer at /dev/fb0 """
    def __init__(self, using_fb=True):
        """Replace path with filename for testing purposes.
        Note that output is in RGB565 though"""
        self.output = None
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self._using_fb = using_fb
        self._bgcolor = BG_COLOR

    def __enter__(self):
        if self._using_fb:
            self.output = open(FB_PATH, "r+b", buffering=0)
            self.output.seek(0)
            self.output.write(clear_bytes(self.size))
        else:
            self.output: Image.Image = clear(self.size, 1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output:
            if self._using_fb:
                # Closig framebuffer device
                self.output.close()
            else:
                # dumping the last buffer to file (maybe not needed)
                self.output.save("__preview/output.png", format="PNG")

    async def render(self, widgets: Dict[str, Widget]):
        """Render and output all layers"""

        async def write_fb(widget: Widget):
            x, y, w, h = (*widget.xy, *widget.size)
            buf = await widget._canvas.asRGB565()
            fb_offset = (y * SCREEN_WIDTH + x) * BYTES_PER_PIXEL
            for row in range(h):
                offset = fb_offset + row * SCREEN_WIDTH * BYTES_PER_PIXEL
                start = row * w * 2
                end = start + w * 2
                self.output.seek(offset)
                self.output.write(buf[start:end])

        elapsed = time.perf_counter()
        dirty = False
        for name, widget in widgets.items():
            if widget.dirty:
                widget.dirty = False
                dirty = True
                if self._using_fb:
                    await write_fb(widget)
                else:
                    self.output.paste(
                        im=widget.image,
                        box=tuple(widget.xy),
                        mask=widget.image.split()[3]
                    )
                logging.info("<%s> updated", name)

        if dirty:
            if not self._using_fb:
                self.output.save("__preview/output.png", format="PNG")
            elapsed = time.perf_counter() - elapsed
            logging.info(f"Refresh routine complete in: {elapsed:.3f} s.")
