import struct
from PIL import Image, ImageDraw

SCREEN_MARGIN = 24
GRID_UNIT = 16
WIDTH = 1920
HEIGHT = 1200

blk = lambda x: x * GRID_UNIT

# Width: blk(117), Height: blk(72)

rgb888_to_rgb565 = lambda r, g, b: ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)



class Screen:

    def __init__(self, mode="RGB", size=(WIDTH, HEIGHT), color=(0, 0, 0)):
        self.image = Image.new(mode, size, color)
        self.canvas = ImageDraw.Draw(self.image)

    def output(self):
        buffer = bytearray()
        pixels = self.image.load()

        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b = pixels[x, y]
                rgb565 = rgb888_to_rgb565(r, g, b)
                buffer += struct.pack("<H", rgb565)

        with open("/dev/fb0", "wb") as f:
            f.write(buffer)