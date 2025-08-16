from core.render import Canvas
from shared.styles import Colors
from typing import Dict

DEFAULT_CONTAINER = (100, 100)
DEFAULT_SCREEN_SIZE = (1920, 1200)
DEFAULT_RADIUS = 24


class Content:
    def __init__(self, xy=(0, 0)):
        self.xy = xy
        self._canvas: Canvas = None
        self._value = None

    def update_value(self, new_value) -> bool:
        if new_value != self._value:
            self._value = new_value
            self._render()
            return True
        return False

    def clone_canvas(self, canvas: Canvas):
        self._canvas = Canvas(canvas._img.size)

    def _render(self) -> Canvas:
        """Renders self at provided canvas (typically at parent's canvas)"""
        return self._canvas


class Container:
    def __init__(self, xy, size, fill, radius, content={}):
        self.xy = xy
        self.fill = fill
        self.radius = radius
        self.content: Dict[str, Content] = content
        self.size = size
        self._canvas: Canvas = Canvas(size)
        for k, v in self.content.items():
            if not isinstance(v, Content):
                raise TypeError(
                    "Unexpected type <%s> for child %s",
                    type(v).__name__, k)
            v.clone_canvas(self._canvas)

    def _render(self):
        """Widget renders itself if it is changed"""
        self._canvas.fill(self.fill, self.radius)
        for child in self.content.values():
            self._canvas.paste(child._canvas(), child.xy)

    @property
    def image(self):
        return self._canvas()


class Text(Content):
    def __init__(self, **kwargs):
        super().__init__()
        self._args = kwargs

    def _render(self):
        self._args["text"] = self._value
        self._canvas.clear().draw.text(**self._args)


class Img(Content):
    def __init__(self, x=0, y=0):
        super().__init__()
        self._position = (x, y)

    def _render(self):
        self._canvas.clear().load(self._value, self._position)


class Rect(Content):
    def __init__(self, xy=(0, 0, 0, 0),
                 fill=Colors.PANEL_BG, radius=DEFAULT_RADIUS):
        super().__init__()
        self._args = {
            "xy": xy,
            "radius": radius,
            "fill": fill
        }

    def clone_canvas(self, canvas: Canvas):
        """Renders rectangle immediately once it got canvas"""
        self._canvas = canvas.copy()
        self._canvas.clear().draw.rounded_rectangle(**self._args)


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
            f"{key}": "" for key in self.content.keys()
        }
        self._name = ""
        self._dirty = False

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
                self._dirty = True

    async def update(self) -> bool:
        """Polls all children. If any child has outdated content, it renders
        itself with new content."""
        if self._dirty:
            for key, item in self.content.items():
                if isinstance(item, Rect):
                    continue
                item.update_value(self._state[key])
            self._render()
            self._dirty = False
            return True
        return False


class WeekProgress(Content):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self._value = "0"

    def _render(self):
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
