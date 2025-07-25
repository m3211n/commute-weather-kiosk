import subprocess
from PIL import Image, ImageDraw, ImageFont
import struct

WIDTH = 1920
HEIGHT = 1200
TEXT = "FUCK OFF HAHAHA!!!"

img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
except:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), TEXT, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_pos = ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2)
draw.text(text_pos, TEXT, font=font, fill=(255, 0, 0))

def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

buffer = bytearray()
pixels = img.load()

for y in range(HEIGHT):
    for x in range(WIDTH):
        r, g, b = pixels[x, y]
        rgb565 = rgb888_to_rgb565(r, g, b)
        buffer += struct.pack("<H", rgb565)

with open("/dev/fb0", "wb") as f:
    f.write(buffer)