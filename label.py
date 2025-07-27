from PIL import Image, ImageDraw, ImageFont
import numpy as np
import asyncio

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def rgb888_to_rgb565_numpy(image):
    arr = np.array(image, dtype=np.uint8)
    r = arr[:, :, 0].astype(np.uint16)
    g = arr[:, :, 1].astype(np.uint16)
    b = arr[:, :, 2].astype(np.uint16)
    rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    return rgb565.astype('<u2').tobytes()

class Label:
    def __init__(self, x, y, text="...", font_size=24, color="white", bg="black"):
        self.font_size = font_size
        self.font = ImageFont.truetype(FONT_PATH, self.font_size)
        self.text(text)
        self.x = x
        self.y = y
        self.color = color
        self.bg = bg

    async def text(self, new_text):
        self._text = new_text
        bbox = self.font.getbbox(self.text) # fallback text if empty
        self.width = bbox[2] - bbox[0]
        self.height = bbox[3] - bbox[1]
        image = self._render(new_text)
        await self._write_to_framebuffer(image)

    def _render(self, new_text):
        image = Image.new("RGB", (self.width, self.height), self.bg)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), new_text, fill=self.color, font=self.font)
        return image

    async def _write_to_framebuffer(self, image):
        buf = await asyncio.to_thread(rgb888_to_rgb565_numpy, image)

        row_size = 1920  # screen width in pixels
        fb_offset = (self.y * row_size + self.x) * 2

        with open("/dev/fb0", "r+b") as f:
            for row in range(self.height):
                offset = fb_offset + row * row_size * 2
                start = row * self.width * 2
                end = start + self.width * 2
                f.seek(offset)
                f.write(buf[start:end])
