from PIL import Image
import numpy as np
import time

WIDTH = 960
HEIGHT = 600

def draw_to_framebuffer(image: Image.Image):
    arr = np.array(image.convert("RGB"))

    # BGR channel extraction (swap red and blue)
    b = arr[:, :, 0] >> 3  # originally red
    g = arr[:, :, 1] >> 2
    r = arr[:, :, 2] >> 3  # originally blue

    rgb565 = (b << 11) | (g << 5) | r  # BGR565

    # Write as big-endian (high byte first)
    buffer = rgb565.astype('>u2').tobytes()

    with open("/dev/fb0", "wb") as f:
        f.write(buffer)

def show_color(color, label):
    img = Image.new("RGB", (WIDTH, HEIGHT), color)
    draw_to_framebuffer(img)
    print(f"Displayed {label}")
    time.sleep(2)

show_color((255, 0, 0), "Red")
show_color((0, 255, 0), "Green")
show_color((0, 0, 255), "Blue")