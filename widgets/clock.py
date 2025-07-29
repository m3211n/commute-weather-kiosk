from datetime import datetime
from widgets.core import Widget, Label
from shared.styles import Colors, Fonts

TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%A, %B %d, %Y"


def _callback(label: Label, f):
    new_text = datetime.now().strftime(f)
    if not label.text == new_text:
        label.text = new_text
        return True
    return False


labelTime = Label(
    xy=(474, 268),
    text="--:--",
    fill=Colors.default,
    font=Fonts.clock,
    anchor="mb",
    callback=lambda: _callback(labelTime, TIME_FORMAT)
)

labelDate = Label(
    xy=(474, 300),
    text="Today",
    fill=Colors.title,
    font=Fonts.title,
    anchor="mt",
    callback=lambda: _callback(labelDate, DATE_FORMAT)
)

clock = Widget(
    position=(8, 8),
    size=(948, 472),
    content=[
        labelTime,
        labelDate
    ])
