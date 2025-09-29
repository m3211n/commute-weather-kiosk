from typing import Tuple
from numpy import zeros

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BG_COLOR,
    FB_PATH,
    BYTES_PER_PIXEL
    )


class FrameBuffer:
    """ Generic screen class to dump buffer at /dev/fb0 """
    def __init__(
            self,
            size: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT),
            path: str = FB_PATH,
            fill: Tuple[int, int, int] = BG_COLOR):
        self.output = open(path, "r+b", buffering=0)
        self.size = size
        self._bgcolor = fill

    def __enter__(self):
        self.output = open(FB_PATH, "r+b", buffering=0)
        self.output.seek(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output:
            self.output.close()

    def clear(self):
        self.output.write(zeros(self.size, dtype="<u2"))

    def write_at(
            self,
            buf: bytes,
            xy: Tuple[int, int],
            size: Tuple[int, int]):
        x, y, w, h = (*xy, *size)
        fb_offset = (y * SCREEN_WIDTH + x) * BYTES_PER_PIXEL
        for row in range(h):
            offset = fb_offset + row * SCREEN_WIDTH * BYTES_PER_PIXEL
            start = row * w * 2
            end = start + w * 2
            self.output.seek(offset)
            self.output.write(buf[start:end])
