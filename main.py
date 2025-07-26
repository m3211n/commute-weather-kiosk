import asyncio
import requests
from PIL import Image
import numpy as np
import io

WIDTH = 1920
HEIGHT = 1200

def draw_to_framebuffer(image: Image.Image):
    arr = np.array(image.convert("RGB"))
    b = arr[:, :, 0] >> 3  # red becomes blue
    g = arr[:, :, 1] >> 2
    r = arr[:, :, 2] >> 3  # blue becomes red

    rgb565 = (b << 11) | (g << 5) | r  # BGR565
    buffer = rgb565.astype('>u2').tobytes()  # big-endian byte order

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def fetch_cat_image() -> Image.Image:
    try:
        response = requests.get("https://cataas.com/cat", timeout=10)
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print("Failed to fetch cat:", e)
        # fallback: blank screen
        return Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))

async def update_loop():
    while True:
        img = fetch_cat_image()
        draw_to_framebuffer(img)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(update_loop())
