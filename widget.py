from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

class Widget:
    def __init__(self, width, height, background="black"):
        self.image = Image.new("RGB", (width, height), background)
        self.draw = ImageDraw.Draw(self.image)

    def text(self, position, text, font_size=24, color="white"):
        font = ImageFont.truetype(FONT_PATH, font_size)
        self.draw.text(position, text, fill=color, font=font)

    def clear(self, color="black"):
        self.draw.rectangle([0, 0, *self.image.size], fill=color)
