from PIL import Image
from app.screen import Screen
import imgkit
import io

TESTING = False

html = '<h1 style="color: red;">Hello, Kiosk</h1>'
imgkit.from_string(html, 'out.png')

screen = Screen()
html = """
<html>
  <body style="margin: 0; padding: 0;">
    <div style="width: 640px; height: 480px; background: black; color: white; display: flex; align-items: center; justify-content: center;">
      <h1>Hello Kiosk</h1>
    </div>
  </body>
</html>
"""

html_image_bytes = imgkit.from_string(html, False)
html_image = Image.open(io.BytesIO(html_image_bytes)).convert("RGB")

# --- resize or position if needed
# html_image = html_image.resize((WIDTH, HEIGHT))  # or center it

# --- paste onto your canvas
screen.image.paste(html_image, (0, 0))  # (x, y) position

# --- flush to framebuffer
screen.output()

if TESTING:
    screen.image.save("__preview/output.png") 
else:
    screen.output()
