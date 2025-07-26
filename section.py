from PIL import Image, ImageDraw

class Section:
    def __init__(self, x, y, width, height, widgets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.widgets = widgets
        self.image = None

    def render(self):
        self.image = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(self.image)
        for widget in self.widgets:
            widget.draw(draw)

    def paste_to(self, canvas: Image.Image):
        if self.image:
            canvas.paste(self.image, (self.x, self.y))