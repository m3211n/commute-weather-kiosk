from PIL import Image
from io import BytesIO
import asyncio
import imgkit

class Section:
    def __init__(self, bg_color="black", x=0, y=0, width=100, height=100, widgets=None):
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.widgets = widgets
        self.image = None

    async def render(self):
        html_parts = [w.get_html() for w in self.widgets if w.get_html()] if self.widgets else [""]
        html = f"""
        <html>
          <body style='margin:0; width:{self.width}px; height:{self.height}px; overflow:hidden; background-color:{self.bg_color}'>
            {''.join(html_parts)}
          </body>
        </html>
        """

        png_bytes = await asyncio.to_thread(
            imgkit.from_string,
            html,
            False,
            options={
                'format': 'png',
                'width': str(self.width),
                'height': str(self.height),
                'disable-smart-width': '',
                'quiet': ''
            }
        )
        self.image = Image.open(BytesIO(png_bytes))

    def paste_to(self, canvas: Image.Image):
        if self.image:
            canvas.paste(self.image, (self.x, self.y))