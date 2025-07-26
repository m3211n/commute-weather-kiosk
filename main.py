import asyncio
# import time
import imgkit
from PIL import Image
import numpy as np
import io
# import requests

WIDTH = 960
HEIGHT = 600
IMGKIT_CONFIG = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

def draw_to_framebuffer(image: Image.Image):
    arr = np.array(image)
    b = arr[:, :, 0] >> 3
    g = arr[:, :, 1] >> 2
    r = arr[:, :, 2] >> 3
    rgb565 = (r << 11) | (g << 5) | b
    with open("/dev/fb0", "wb") as f:
        f.write(rgb565.astype('<u2').tobytes())

def build_html():
    return f"""
<html>
<head>
  <style>
    body {{
      background-color: black;
      color: white;
      margin: 0;
      padding: 0;
    }}
    img {{
      display: block;
      margin: auto;
    }}
    .label {{
      text-align: center;
      font-family: sans-serif;
      font-size: 28px;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <div class="label">Weather in Stockholm</div>
  <img src="https://wttr.in/Stockholm.png?m&lang=en&1" />
</body>
</html>
"""

def html_to_image(html: str) -> Image.Image:
    png_data = imgkit.from_string(html, False, config=IMGKIT_CONFIG, options={
        'format': 'png',
        'width': '960',
        'height': '400',
        'disable-smart-width': '',
        'load-error-handling': 'ignore',
        'javascript-delay': '1000'
    })
    return Image.open(io.BytesIO(png_data)).convert("RGB")

async def update_loop():
    while True:
        html = build_html()
        img = html_to_image(html)

        screen = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        screen.paste(img, (0, 100))  # Adjust vertical position

        draw_to_framebuffer(screen)
        await asyncio.sleep(900)  # update every 15 minutes

if __name__ == "__main__":
    asyncio.run(update_loop())
