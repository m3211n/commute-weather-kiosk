from PIL import Image

class Section:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.image = Image.new("RGB", (width, height), "black")

    def add(self, x, y, widget):
        self.image.paste(widget.image, (x, y))

    def paste_to(self, canvas):
        canvas.paste(self.image, (self.x, self.y))