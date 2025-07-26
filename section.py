from PIL import Image

class Section:
    def __init__(self, x, y, width, height, background="black"):
        self.x = x
        self.y = y
        self.image = Image.new("RGB", (width, height), background)

    def add(self, x, y, widget):
        self.image.paste(widget.image, (x, y))
