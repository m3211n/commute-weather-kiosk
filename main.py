import asyncio
import requests
from PIL import Image
import io
import numpy as np
import struct

WIDTH = 1920
HEIGHT = 1200

def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def draw_test_colors():
    """Draw test pattern with different color combinations to debug"""
    buffer = bytearray()
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x < WIDTH // 6:
                # Pure Red
                r, g, b = 255, 0, 0
            elif x < WIDTH // 3:
                # Pure Blue  
                r, g, b = 0, 0, 255
            elif x < WIDTH // 2:
                # Pure Green
                r, g, b = 0, 255, 0
            elif x < 2 * WIDTH // 3:
                # Cyan (Green + Blue)
                r, g, b = 0, 255, 255
            elif x < 5 * WIDTH // 6:
                # Magenta (Red + Blue)
                r, g, b = 255, 0, 255
            else:
                # Yellow (Red + Green)
                r, g, b = 255, 255, 0
            
            # Try different bit layout - maybe not standard RGB565
            # Your framebuffer might need a different format entirely
            rgb565 = ((g & 0xF8) << 8) | ((r & 0xFC) << 3) | ((b & 0xF8) >> 3)
            buffer += struct.pack("<H", rgb565)  # little-endian with GRB

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def draw_to_framebuffer(image: Image.Image):
    img = image.convert("RGB").resize((WIDTH, HEIGHT))
    pixels = np.array(img)
    
    buffer = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[y, x]
            # Use GRB format (G→R position, R→G position, B→B position)
            rgb565 = ((g & 0xF8) << 8) | ((r & 0xFC) << 3) | ((b & 0xF8) >> 3)
            buffer += struct.pack("<H", rgb565)  # little-endian

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
    # First test with solid colors
    draw_test_colors()
    await asyncio.sleep(10)  # Show test pattern for 10 seconds
    
    while True:
        cat = fetch_cat_image()
        draw_to_framebuffer(cat)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(update_loop())
