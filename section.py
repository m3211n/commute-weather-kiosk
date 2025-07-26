from PIL import Image

class Section(Image.Image):
    def __new__(cls, x, y, width, height):
        obj = Image.new("RGB", (width, height), "black")
        obj.__class__ = cls
        obj.x = x
        obj.y = y
        return obj

    def add(self, x, y, widget):
        self.paste(widget.image, (x, y))

    def paste_to(self, canvas):
        canvas.paste(self, (self.x, self.y))