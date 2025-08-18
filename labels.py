from core.ui import Text, StaticText
from shared.styles import Fonts, Colors
# import logging


def time(x, y, anchor="mt"):
    return Text(
        xy=(x, y),
        font=Fonts.font("bold", 216),
        fill=Colors.DEFAULT,
        anchor=anchor)


def date(x, y, anchor="mt"):
    return Text(
        xy=(x, y),
        font=Fonts.font("bold", 40),
        fill=Colors.DEFAULT,
        anchor=anchor)


def temp_now(x, y, anchor="lt", accent=True):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("light", 200),
        fill=fill,
        anchor=anchor)


def label_40(x, y, anchor="rt", accent=True, static_value=None):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    params = {
        "xy": (x, y),
        "font": Fonts.font("regular", 40),
        "fill": fill,
        "anchor": anchor
    }
    if static_value:
        return StaticText(value=static_value, **params)
    return Text(**params)


def label_68(x, y, anchor="lt", accent=True, static_value=None):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    params = {
        "xy": (x, y),
        "font": Fonts.font("regular", 68),
        "fill": fill,
        "anchor": anchor
    }
    if static_value:
        return StaticText(value=static_value, **params)
    return Text(**params)


def static_icon(x, y, value, anchor="lt", accent=True):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return StaticText(
        value=value,
        xy=(x, y),
        font=Fonts.font("icon", 36),
        fill=fill,
        anchor=anchor)


def h3_block(x, y, accent=True, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("regular", 32),
        fill=color,
        features=["tnum"],
        **kwargs)


def icons_block(x, y, accent=True, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("icon", 36),
        fill=color,
        **kwargs)


def h3(x, y, anchor="rt", accent=False, static_value=None):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    params = {
        "xy": (x, y),
        "font": Fonts.font("regular", 32),
        "fill": color,
        "anchor": anchor,
        "features": ["tnum"]
    }
    if static_value:
        return StaticText(value=static_value, **params)
    return Text(**params)


def h4(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H4,
        fill=color,
        features=["tnum"],
        anchor=anchor)


def departure_block(x, y, **kwargs):
    return Text(
        xy=(x, y),
        font=Fonts.font("bold", 48),
        fill=Colors.DEPARTURES,
        features=["tnum"],
        **kwargs
    )


def line_block(x, y, **kwargs):
    return Text(
        xy=(x, y),
        font=Fonts.font("regular", 48),
        fill=Colors.DEFAULT,
        features=["tnum"],
        **kwargs
    )


def dest_block(x, y, **kwargs):
    return Text(
        xy=(x, y),
        font=Fonts.font("regular", 48),
        fill=Colors.SECONDARY,
        features=["tnum"],
        **kwargs
    )


def status(x, y, anchor="lm"):
    return Text(
        xy=(x, y),
        font=Fonts.STATUS,
        fill=Colors.TITLE,
        anchor=anchor)


def d2(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.D2,
        fill=Colors.DEPARTURES,
        anchor=anchor)
