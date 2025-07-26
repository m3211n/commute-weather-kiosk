import asyncio
import time
import subprocess
from PIL import Image
import imgkit
import numpy as np

WIDTH = 960
HEIGHT = 600
HTML_WIDTH = 800  # logical size for HTML render
HTML_HEIGHT = 200
START_TIME = time.time()

# Path to wkhtmltoimage binary
IMGKIT_CONFIG = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

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

def html_to_image(html: str) -> Image.Image:
    # Render HTML to temporary file
    img_data = imgkit.from_string(html, False, config=IMGKIT_CONFIG, options={
        'format': 'png',
        'width': str(HTML_WIDTH),
        'height': str(HTML_HEIGHT),
        'disable-smart-width': ''
    })
    return Image.open(io.BytesIO(img_data)).convert("RGB")

def draw_to_framebuffer(image: Image.Image):
    arr = np.array(image)
    r = arr[:, :, 0] >> 3
    g = arr[:, :, 1] >> 2
    b = arr[:, :, 2] >> 3
    rgb565 = (r << 11) | (g << 5) | b
    with open("/dev/fb0", "wb") as f:
        f.write(rgb565.astype('<u2').tobytes())

def build_html(elapsed: int, temp: str, ram: str, delta_ms: int) -> str:
    return f"""
    <html>
    <head>
        <style>
            body {{
                background: black;
                color: white;
                font-family: Arial, sans-serif;
                font-size: 24px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #444;
            }}
        </style>
    </head>
    <body>
        <table>
            <tr><td>Uptime</td><td>{elapsed} sec</td></tr>
            <tr><td>CPU Temp</td><td>{temp}</td></tr>
            <tr><td>Free RAM</td><td>{ram}</td></tr>
            <tr><td>Render Time</td><td>{delta_ms} ms</td></tr>
        </table>
    </body>
    </html>
    """

async def update_loop():
    while True:
        t0 = time.time()

        elapsed = int(t0 - START_TIME)
        temp = get_cpu_temp()
        ram = get_free_mem()

        html = build_html(elapsed, temp, ram, 0)
        img = html_to_image(html)

        # Create base screen
        screen = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        screen.paste(img, (int((WIDTH - HTML_WIDTH) / 2), 100))  # center horizontally

        t1 = time.time()
        delta_ms = int((t1 - t0) * 1000)

        # Update render time in HTML and re-render just that part
        html = build_html(elapsed, temp, ram, delta_ms)
        img = html_to_image(html)
        screen.paste(img, (int((WIDTH - HTML_WIDTH) / 2), 100))

        draw_to_framebuffer(screen)

        await asyncio.sleep(2)

if __name__ == "__main__":
    import io
    asyncio.run(update_loop())
