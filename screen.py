import numpy as np
import asyncio

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200


def rgb888_to_rgb565_numpy(image):
    """Convert image from RGB888 to RGB565 for /dev/fb0 on Pi Zero 2W"""
    # ensures RGB mode, shape (H, W, 3), dtype=uint8
    arr = np.asarray(image.convert("RGB"))
    # single cast for all channels
    arr16 = arr.astype(np.uint16)

    r = (arr16[:, :, 0] & 0xF8) << 8         # 5 bits
    g = (arr16[:, :, 1] & 0xFC) << 3         # 6 bits
    b = (arr16[:, :, 2] & 0xF8) >> 3         # 5 bits

    rgb565 = r | g | b
    return rgb565.astype('<u2').tobytes()   # little-endian for /dev/fb0


class Screen:
    """Generic screen class"""
    def __init__(
            self,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            bgcolor=(0, 0, 0)
    ):
        self.width = width
        self.height = height
        self.fb = None
        self.widgets = []
        self._bgcolor = bgcolor

    def __enter__(self):
        self.fb = open("/dev/fb0", "r+b", buffering=0)
        buf = np.zeros((self.width, self.height), dtype="<u2")
        self.fb.seek(0)
        self.fb.write(buf)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fb:
            self.fb.close()

    async def refresh_all(self, dirty_only=True) -> str:
        """Render and draw all layers to the framebuffer"""
        for widget in self.widgets:
            is_dirty = widget.render()
            if (dirty_only and is_dirty) or (not dirty_only):
                image = widget.image
                img_w, img_h = image.size
                pos_x, pos_y = widget.position
                buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, image)
                row_size = self.width
                fb_offset = (pos_y * row_size + pos_x) * 2
                for row in range(img_h):
                    offset = fb_offset + row * row_size * 2
                    start = row * img_w * 2
                    end = start + img_w * 2
                    self.fb.seek(offset)
                    self.fb.write(buf[start:end])
                return f"Dirty widget {widget.__class__.__name__} was redrawn."
            else:
                return "All widgets clean. Sleepin'..."
