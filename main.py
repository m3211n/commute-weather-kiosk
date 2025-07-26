import requests
from PIL import Image
import numpy as np
from io import BytesIO
import time

FB_WIDTH = 1920
FB_HEIGHT = 1200
FB_DEVICE = "/dev/fb0"
REFRESH_INTERVAL = 5  # seconds

def fetch_random_cat_image() -> Image.Image:
    url = "https://cataas.com/cat"  # Random cat image
    response = requests.get(url, timeout=10)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image

def draw_to_framebuffer(image: Image.Image):
    # Resize image to match framebuffer resolution
    image = image.resize((FB_WIDTH, FB_HEIGHT), Image.Resampling.LANCZOS)

    # Convert to RGB565 format
    arr = np.array(image)
    r = arr[:, :, 0] >> 3
    g = arr[:, :, 1] >> 2
    b = arr[:, :, 2] >> 3
    rgb565 = (r << 11) | (g << 5) | b
    buffer = rgb565.astype('>u2').tobytes()  # big endian

    with open(FB_DEVICE, "wb") as f:
        f.write(buffer)

def main():
    while True:
        try:
            img = fetch_random_cat_image()
            draw_to_framebuffer(img)
        except Exception as e:
            print("Error:", e)
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()