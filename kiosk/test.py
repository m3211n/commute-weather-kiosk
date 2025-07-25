from PIL import Image
import struct

WIDTH = 1920
HEIGHT = 1200
COLOR = (0, 0, 255)  # Blue in RGB888

# Create an RGB image
img = Image.new("RGB", (WIDTH, HEIGHT), COLOR)
pixels = img.load()

# Convert to RGB565 manually
def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# Create byte buffer
buffer = bytearray()

for y in range(HEIGHT):
    for x in range(WIDTH):
        r, g, b = pixels[x, y]
        rgb565 = rgb888_to_rgb565(r, g, b)
        buffer += struct.pack("<H", rgb565)  # Little-endian 16-bit

# Write to framebuffer
with open("/dev/fb0", "wb") as f:
    f.write(buffer)
