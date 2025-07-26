import asyncio
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 1200
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

def draw_to_framebuffer(image: Image.Image):
    buffer = bytearray()
    pixels = image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            buffer += rgb565.to_bytes(2, 'little')
    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

async def update_loop():
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    while True:
        elapsed = int(time.time() - start_time)
        temp = get_cpu_temp()
        ram = get_free_mem()

        img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        lines = [
            f"{elapsed} seconds since start",
            f"CPU Temp: {temp}",
            f"Free RAM: {ram}"
        ]

        for i, line in enumerate(lines):
            draw.text((50, 100 + i * 60), line, font=font, fill=COLOR_TEXT)

        draw_to_framebuffer(img)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(update_loop())
