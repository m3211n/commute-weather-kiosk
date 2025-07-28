import imgkit
import io
import time
from PIL import Image

WIDTH = 1920
HEIGHT = 1200
TILE_WIDTH = 240
TILE_HEIGHT = 600
ROWS = 2
COLS = 4

HTML_TEMPLATE = """
<html><body style='margin:0; background:black; color:white; font-size:40px;'>
  <div style='display:flex; justify-content:center; align-items:center; height:100%;'>
    <p>{}</p>
  </div>
</body></html>
"""

def render_html(html: str, width: int, height: int) -> Image.Image:
    options = {
        "width": width,
        "height": height,
        "disable-smart-width": "",
        "format": "png"
    }
    png_bytes = imgkit.from_string(html, False, options=options)
    return Image.open(io.BytesIO(png_bytes))

def benchmark_fullscreen():
    html = HTML_TEMPLATE.format("FULLSCREEN 1920x1200")
    start = time.time()
    img = render_html(html, WIDTH, HEIGHT)
    duration = time.time() - start
    print(f"Full-screen render time: {duration:.3f} s")
    return img

def benchmark_tiles():
    durations = []
    for i in range(ROWS * COLS):
        html = HTML_TEMPLATE.format(f"TILE {i}")
        start = time.time()
        _ = render_html(html, TILE_WIDTH, TILE_HEIGHT)
        durations.append(time.time() - start)
    total_time = sum(durations)
    print(f"8x TILE render time (sum): {total_time:.3f} s")
    print(f"Average tile render time: {total_time / (ROWS * COLS):.3f} s")
    return durations

if __name__ == "__main__":
    print("Benchmarking HTML rendering with imgkit...")
    benchmark_fullscreen()
    benchmark_tiles()
