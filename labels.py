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


def temp_now(x, y, anchor="lt", accent=False):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("light", 200),
        fill=fill,
        anchor=anchor)


def feels_like(x, y, anchor="rt", accent=False):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("regular", 40),
        fill=fill,
        anchor=anchor)


def static_icon(x, y, value, anchor="lt", accent=True):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return StaticText(
        value=value,
        xy=(x, y),
        font=Fonts.font("icon", 36),
        fill=fill,
        anchor=anchor)


def h3_block(x, y, accent=False, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H3,
        fill=color,
        features=["tnum"],
        **kwargs)


def icons_block(x, y, accent=False, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.font("icon", 36),
        fill=color,
        **kwargs)


def h3(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H3,
        fill=color,
        features=["tnum"],
        anchor=anchor)


def h4(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H4,
        fill=color,
        features=["tnum"],
        anchor=anchor)


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


def d3(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.D3,
        fill=Colors.SECONDARY,
        anchor=anchor)
