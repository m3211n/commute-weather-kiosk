from core.render import Canvas
from core.styles import Colors
from typing import Dict

DEFAULT_CONTAINER = (100, 100)
DEFAULT_SCREEN_SIZE = (1920, 1200)
DEFAULT_RADIUS = 24


class Content:
    def __init__(self, xy=(0, 0), value=None):
        self.xy = xy
        self.static = True if value else False
        self.value = value

    def update_value(self, new_value) -> bool:
        if new_value != self.value:
            self.value = new_value
            return True
        return False

    def render(self, canvas: Canvas) -> Canvas:
        """Renders self at provided canvas (typically at parent's canvas)"""
        return canvas()


class Container:
    def __init__(self, xy, size, fill, radius, content={}):
        self.xy = xy
        self.fill = fill
        self.radius = radius
        self.content: Dict[str, Content] = content
        self.size = size
        self._canvas: Canvas = Canvas(size)

    def render(self):
        """Widget renders itself if it is changed"""
        self._canvas.fill(self.fill, self.radius)
        for child in self.content.values():
            child_canvas: Canvas = self._canvas.copy()
            self._canvas.paste(child.render(child_canvas), child.xy)

    @property
    def image(self):
        return self._canvas()


class Text(Content):
    def __init__(self, value=None, **kwargs):
        super().__init__(value=value)
        self._args = kwargs

    def render(self, canvas):
        self._args["text"] = self.value
        canvas.clear().draw.multiline_text(**self._args)
        return canvas()


class ImageView(Content):
    def __init__(self, x=0, y=0, value=None):
        super().__init__(value=value)
        self._position = (x, y)

    def render(self, canvas) -> Canvas:
        canvas.clear().load(self.value, self._position)
        return canvas()


class Rect(Content):
    def __init__(self, xy=(0, 0, 0, 0),
                 fill=Colors.panel_bg, radius=DEFAULT_RADIUS):
        super().__init__()
        self._args = {
            "xy": xy,
            "radius": radius,
            "fill": fill
        }

    def render(self, canvas):
        canvas.clear().draw.rounded_rectangle(**self._args)
        return canvas()


class Widget(Container):
    def __init__(self, content={},
                 size=DEFAULT_CONTAINER, xy=(0, 0),
                 fill=(0, 0, 0, 0), radius=0):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(
            content=content,
            xy=xy, size=size, fill=fill, radius=radius)
        self._state = {
            key: "" for key in self.content.keys()
        }
        self._name = ""
        self.dirty = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: dict):
        for k, v in new_state.items():
            if not (k in self._state.keys()):
                raise ValueError(
                    f"Widget <{self._name}> got unknown key <{k}>",
                )
            if not isinstance(v, str):
                raise TypeError(
                    f"Expected <str>. Got <{type(v).__name__}>",
                )
            if self._state[k] != new_state[k]:
                self._state[k] = v
                self.dirty = True
        if self.dirty:
            for key, item in self.content.items():
                if not item.static:
                    item.update_value(self._state[key])
            self.render()

    async def update(self) -> bool:
        """Polls all children. If any child has outdated content, it renders
        itself with new content."""
        if self.dirty:
            for key, item in self.content.items():
                if item.static:
                    continue
                item.update_value(self._state[key])
            self.render()
            self.dirty = False
            return True
        return False


class WeekProgress(Content):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self._value = "0"

    def render(self):
        numb = int(self._value)
        self._canvas.clear()
        for i in range(7):
            if numb >= (i + 1):
                fill = Colors.DEFAULT
            else:
                fill = (0, 0, 0, 0)
            self._canvas.draw.circle(
                xy=(self.x + 10 + i * 36, self.y + 10),
                radius=10,
                fill=fill,
                outline=Colors.DEFAULT,
                width=2)
