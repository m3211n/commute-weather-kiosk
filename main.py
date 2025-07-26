import asyncio
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 960
HEIGHT = 600
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust if needed
FONT_SIZE = 48
COLOR_BG = (0, 0, 0)
COLOR_TEXT = (255, 255, 255)

start_time = time.time()

def get_cpu_temp():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return output.strip().replace("temp=", "")
    except:
        return "N/A"

def get_free_mem():
    try:
        output = subprocess.check_output(["free", "-m"]).decode().splitlines()
        mem_line = output[1].split()
        return f"{mem_line[3]} MB"
    except:
        return "N/A"

import numpy as np

def draw_to_framebuffer(image: Image.Image):
    arr = np.array(image.convert("RGB"))
    r = arr[:, :, 0] >> 3
    g = arr[:, :, 1] >> 2
    b = arr[:, :, 2] >> 3

    rgb565 = (r << 11) | (g << 5) | b
    buffer = rgb565.astype('<u2').tobytes()  # little-endian, no swap

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

async def update_loop():
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    prev_time = time.time()

    while True:
        now = time.time()
        elapsed = int(now - start_time)
        delta_ms = int((now - prev_time) * 1000)
        prev_time = now

        temp = get_cpu_temp()
        ram = get_free_mem()

        img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        lines = [
            f"{elapsed} seconds since start",
            f"CPU Temp: {temp}",
            f"Free RAM: {ram}",
            f"Last update: {delta_ms} ms ago"
        ]

        for i, line in enumerate(lines):
            draw.text((50, 100 + i * 60), line, font=font, fill=COLOR_TEXT)

        draw_to_framebuffer(img)

if __name__ == "__main__":
    asyncio.run(update_loop())
