import asyncio
import requests
from PIL import Image
import io
import numpy as np

WIDTH = 1920
HEIGHT = 1200

def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def draw_to_framebuffer(image: Image.Image):
    img = image.convert("RGB").resize((WIDTH, HEIGHT))
    pixels = np.array(img)
    
    buffer = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[y, x]
            # Swap R and B for BGR565
            rgb565 = rgb888_to_rgb565(r, g, b)
            buffer += int(rgb565).to_bytes(2, byteorder='big')  # write as big-endian

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def fetch_cat_image():
    try:
        response = requests.get("https://cataas.com/cat", timeout=10)
        return Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as e:
        print("Failed to fetch cat:", e)
        return Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # fallback

async def update_loop():
    while True:
        cat = fetch_cat_image()
        draw_to_framebuffer(cat)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(update_loop())
