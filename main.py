import asyncio
import requests
from PIL import Image
import numpy as np
import io

WIDTH = 1920
HEIGHT = 1200
CAT_URL = "https://cataas.com/cat"

def rgb_to_rgb565(image: Image.Image) -> bytes:
    """Convert PIL RGB image to raw RGB565 bytes."""
    img = image.convert("RGB")
    arr = np.array(img)

    r = arr[:, :, 0] >> 3
    g = arr[:, :, 1] >> 2
    b = arr[:, :, 2] >> 3

    rgb565 = (r << 11) | (g << 5) | b
    return rgb565.astype('>u2').tobytes()  # >u2 = big-endian 16-bit

def draw_to_framebuffer(image: Image.Image):
    """Write RGB565 image to /dev/fb0."""
    try:
        fb_data = rgb_to_rgb565(image)
        with open("/dev/fb0", "wb") as f:
            f.write(fb_data)
    except Exception as e:
        print("Framebuffer write error:", e)

def fetch_cat_image() -> Image.Image:
    """Download and resize cat image. Return black fallback if it fails."""
    try:
        response = requests.get(CAT_URL, timeout=10)
        img = Image.open(io.BytesIO(response.content))
        return img.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    except Exception as e:
        print("Failed to fetch cat image:", e)
        return Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))

async def update_loop():
    while True:
        img = fetch_cat_image()
        draw_to_framebuffer(img)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(update_loop())