import logging
import time

from typing import List
from shared.rgb565 import rgb888_to_rgb565_numpy as convert
from shared.rgb565 import clear as black
from widgets.core import Widget

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
BYTES_PER_PIXEL = 2
BG_COLOR = (0, 0, 0)


class Screen:
    """ Generic screen class to dump buffer at /dev/fb0 """
    def __init__(self, path="/dev/fb0"):
        """Replace path with filename for testing purposes.
        Note that output is in RGB565 though"""
        self.path = path
        self.fb = None
        self.widgets: List[Widget] = []
        self._bgcolor = BG_COLOR

    def __enter__(self):
        self.fb = open(self.path, "r+b", buffering=0)
        self.fb.seek(0)
        self.fb.write(black((SCREEN_WIDTH, SCREEN_HEIGHT)))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fb:
            self.fb.close()

    async def _decode_and_write(self, widget: Widget):
        x, y, w, h = (*widget.position, *widget.size)
        elapsed = time.perf_counter()
        buf = await convert(widget.image)
        fb_offset = (y * SCREEN_WIDTH + x) * BYTES_PER_PIXEL
        for row in range(h):
            offset = fb_offset + row * SCREEN_WIDTH * BYTES_PER_PIXEL
            start = row * w * 2
            end = start + w * 2
            self.fb.seek(offset)
            self.fb.write(buf[start:end])
        elapsed = time.perf_counter() - elapsed
        msg = f"Widget {widget.__class__.__name__} rendered updated content."
        logging.info(msg)
        logging.debug(f"{msg} Render time: {elapsed:.3f} s.")

    async def refresh(self, only_dirty=True):
        """Render and draw all layers to the framebuffer"""
        elapsed = time.perf_counter()

        for widget in self.widgets:
            widget_is_dirty = await widget.maybe_render()
            if (only_dirty and widget_is_dirty) or (not only_dirty):
                await self._decode_and_write(widget)
            else:
                logging.debug("Nothing to redraw, just sleepin...")

        elapsed = time.perf_counter() - elapsed
        logging.debug(f"Refresh routine complete in: {elapsed:.3f} s.")
