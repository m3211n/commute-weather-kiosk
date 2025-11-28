from core.render import Canvas
from core.ui import Content

DEFAULT_SIZE = (100, 100)
DEFAULT_RADIUS = 24
MODE = "RGBA"


class Widget:
    def __init__(
            self, size=DEFAULT_SIZE, xy=(0, 0), fill=(0, 0, 0, 0), radius=0
            ):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        self.xy = xy
        self.size = size
        self.children: dict[str, Content] = {}
        self.fill = fill
        self.radius = radius
        self.canvas: Canvas = Canvas(size, MODE)

    @property
    def canvas(self):
        return self.canvas()

    async def _render(self):
        """Widget renders itself if it is changed"""
        self.canvas.fill(self.fill, self.radius)
        for child in self.children.values():
            if isinstance(child, Widget):
                self.canvas.paste(child.canvas, child.xy)
            elif isinstance(child, Content):
                # If widget was changed, it renders its content
                child_canvas = child.paint_at_box(Canvas(self.size, MODE))
                self.canvas.paste(child_canvas)
            else:
                pass

    async def update(self, new_content: dict):
        changed = False
        for key, item in self.children.items():
            if await item.update_value(new_content[key]):
                changed = True
        if changed:
            await self._render()
            return True
        return False
