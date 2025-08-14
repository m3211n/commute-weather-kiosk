from core.render import Canvas
from shared.styles import Fonts, Colors
from typing import Dict, Union

DEFAULT_CONTAINER = (100, 100)
DEFAULT_SCREEN_SIZE = (1920, 1200)
DEFAULT_RADIUS = 24
MODE = "RGBA"


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
        self._canvas = canvas.copy()

    def _render(self) -> Canvas:
        """Renders self at provided canvas (typically at parent's canvas)"""
        return self._canvas


class Container:
    def __init__(self, xy, size, fill, radius, children={}):
        self.xy = xy
        self.fill = fill
        self.radius = radius
        self.children: Dict[str, Union[Content, Container]] = children
        self.size = size
        self._canvas: Canvas = Canvas(size, MODE)
        for k, v in self.children.items():
            if not isinstance(v, Content):
                raise TypeError(
                    "Unexpected type <%s> for child %s",
                    type(v).__name__, k)
            v.clone_canvas(self._canvas)

    def _render(self):
        """Widget renders itself if it is changed"""
        self._canvas.fill(self.fill, self.radius)
        for child in self.children.values():
            self._canvas.paste(child._canvas(), child.xy)

    @property
    def image(self):
        return self._canvas()


class Text(Content):
    def __init__(self, xy=(0, 0),
                 font=Fonts.VALUE, color=Colors.DEFAULT, anchor="lt"):
        super().__init__()
        self._args = {
            "xy": xy,
            "font": font,
            "fill": color,
            "anchor": anchor
        }

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
    def __init__(self, children={},
                 size=DEFAULT_CONTAINER, xy=(0, 0),
                 fill=(0, 0, 0, 0), radius=0):
        """Initializes widget. If image is provided, then background color
        is ignored."""
        super().__init__(
            children=children,
            xy=xy, size=size, fill=fill, radius=radius)
        self._state = {
            f"{key}": "" for key in self.children.keys()
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
                    "Expected <str>. Got <%s>",
                    type(v).__name__)
            if self._state[k] != new_state[k]:
                self._state[k] = v
                self._dirty = True

    async def update(self) -> bool:
        """Polls all children. If any child has outdated content, it renders
        itself with new content."""
        if self._dirty:
            for key, item in self.children.items():
                if isinstance(item, Rect):
                    continue
                item.update_value(self._state[key])
            self._render()
            self._dirty = False
            return True
        return False
