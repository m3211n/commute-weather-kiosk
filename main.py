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
    """Draw test pattern with solid colors to debug"""
    buffer = bytearray()
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x < WIDTH // 3:
                # Red section - should appear red
                r, g, b = 255, 0, 0
            elif x < 2 * WIDTH // 3:
                # Green section - should appear green  
                r, g, b = 0, 255, 0
            else:
                # Blue section - should appear blue
                r, g, b = 0, 0, 255
            
            # Use BRG format with correct bit operations for RGB565
            # B→R position (5 bits), R→G position (6 bits), G→B position (5 bits)
            rgb565 = ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | ((g & 0xF8) >> 3)
            buffer += struct.pack(">H", rgb565)  # big-endian 16-bit

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def draw_to_framebuffer(image: Image.Image):
    img = image.convert("RGB").resize((WIDTH, HEIGHT))
    pixels = np.array(img)
    
    buffer = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[y, x]
            # Use BRG format with correct bit operations for RGB565
            # B→R position (5 bits), R→G position (6 bits), G→B position (5 bits)
            rgb565 = ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | ((g & 0xF8) >> 3)
            buffer += struct.pack(">H", rgb565)  # big-endian 16-bit

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
