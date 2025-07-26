import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
import struct
import datetime

WIDTH = 1920
HEIGHT = 1200

def rgb888_to_rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def draw_test_colors():
    buffer = bytearray()
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x < WIDTH // 6:
                r, g, b = 255, 0, 0
            elif x < WIDTH // 3:
                r, g, b = 0, 0, 255
            elif x < WIDTH // 2:
                r, g, b = 0, 255, 0
            elif x < 2 * WIDTH // 3:
                r, g, b = 0, 255, 255
            elif x < 5 * WIDTH // 6:
                r, g, b = 255, 0, 255
            else:
                r, g, b = 255, 255, 0
            
            rgb565 = ((g & 0xF8) << 8) | ((r & 0xFC) << 3) | ((b & 0xF8) >> 3)
            buffer += struct.pack("<H", rgb565)

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def draw_to_framebuffer(image: Image.Image):
    img = image.resize((WIDTH, HEIGHT))
    
    # Add timestamp text
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text((50, 50), f"Updated: {timestamp}", font=font, fill=(255, 255, 255))
    
    pixels = np.array(img)
    
    buffer = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[y, x]
            # Correct mapping: R→G, G→R, B→B
            # So put G in R position, R in G position, B in B position
            rgb565 = ((g & 0xF8) << 8) | ((r & 0xFC) << 3) | ((b & 0xF8) >> 3)
            buffer += struct.pack("<H", rgb565)

    with open("/dev/fb0", "wb") as f:  
        f.write(buffer)

def fetch_cat_image():
    try:
        response = requests.get("https://cataas.com/cat", timeout=10)
        return Image.open(io.BytesIO(response.content))
    except Exception as e:
        print("Failed to fetch cat:", e)
        return Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # fallback

def debug_color_conversion(image: Image.Image):
    """Save what the image looks like after our color conversion"""
    img = image.convert("RGB").resize((WIDTH, HEIGHT))
    pixels = np.array(img)
    
    # Apply our RBG conversion in reverse to see what we're actually displaying
    converted_pixels = np.zeros_like(pixels)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[y, x]
            # Our conversion: R→G, B→R, G→B
            # So to see what we display: R→G, B→R, G→B
            converted_pixels[y, x] = [b, r, g]  # RBG -> RGB for display
    
    converted_img = Image.fromarray(converted_pixels.astype(np.uint8))
    converted_img.save("converted_cat.png")

async def update_loop():
    while True:
        cat = fetch_cat_image()
        cat.save("original_cat.png")
        debug_color_conversion(cat)
        draw_to_framebuffer(cat)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(update_loop())
