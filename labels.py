from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def time(x, y, anchor="mt"):
    return Text(
        xy=(x, y),
        font=Fonts.D1,
        fill=Colors.DEFAULT,
        anchor=anchor)


def date(x, y, anchor="mt"):
    return Text(
        xy=(x, y),
        font=Fonts.D4,
        fill=Colors.DEFAULT,
        anchor=anchor)


def h1(x, y, anchor="lt", accent=False):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H1,
        fill=fill,
        anchor=anchor)


def h2(x, y, anchor="rt", accent=False):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.H2,
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
        font=Fonts.ICON_XSMALL,
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
