import logging
import time

from typing import List
from core.rgb565 import rgb888_to_rgb565_numpy as convert, clear, clear_rgb
from core.rgb565 import Image
from core.ui import ColorWidget

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
BYTES_PER_PIXEL = 2
FB_PATH = "/dev/fb0"
BG_COLOR = (0, 0, 0)


class Screen:
    """ Generic screen class to dump buffer at /dev/fb0 """
    def __init__(self, using_fb=True):
        """Replace path with filename for testing purposes.
        Note that output is in RGB565 though"""
        self.output = None
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self._using_fb = using_fb
        self.widgets: List[ColorWidget] = []
        self._bgcolor = BG_COLOR

    def __enter__(self):
        if self._using_fb:
            self.output = open(FB_PATH, "r+b", buffering=0)
            self.output.seek(0)
            self.output.write(clear(self.size))
        else:
            self.output: Image = clear_rgb(self.size)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output:
            if self._using_fb:
                # Closig framebuffer device
                self.output.close()
            else:
                # dumping the last buffer to file (maybe not needed)
                self.output.save("__preview/output.png", format="PNG")

    async def _decode_and_write(self, widget: ColorWidget):
        x, y, w, h = (*widget.xy, *widget.size)
        elapsed = time.perf_counter()
        buf = await convert(widget.image)
        fb_offset = (y * SCREEN_WIDTH + x) * BYTES_PER_PIXEL
        for row in range(h):
            offset = fb_offset + row * SCREEN_WIDTH * BYTES_PER_PIXEL
            start = row * w * 2
            end = start + w * 2
            self.output.seek(offset)
            self.output.write(buf[start:end])
        elapsed = time.perf_counter() - elapsed
        msg = f"Widget {widget.__class__.__name__} rendered updated content."
        logging.info(msg)
        logging.debug(f"{msg} Render time: {elapsed:.3f} s.")

    async def refresh(self, only_dirty=True):
        """Render and output all layers"""
        elapsed = time.perf_counter()
        dirty = False
        for widget in self.widgets:
            widget_is_dirty = await widget.maybe_render()
            if (only_dirty and widget_is_dirty) or (not only_dirty):
                dirty = True
                if self._using_fb:
                    await self._decode_and_write(widget)
                else:
                    self.output.paste(widget.image, widget.xy)
                logging.info(
                    "Widget <%s> was updated.",
                    widget.__class__.__name__)
            else:
                logging.debug("Nothing to redraw, just sleepin...")

        if dirty and not self._using_fb:
            self.output.save("__preview/output.png", format="PNG")

        elapsed = time.perf_counter() - elapsed
        logging.debug(f"Refresh routine complete in: {elapsed:.3f} s.")
