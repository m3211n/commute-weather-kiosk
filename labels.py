from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def clock(x, y):
    return Text((x, y), Fonts.CLOCK)


def temp_now(x, y):
    return Text((x, y), Fonts.WEATHER_TODAY)


def small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_SMALL, color, anchor)


def small_block(x, y, accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_SMALL, color)


def x_small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_XSMALL, color, anchor)


def title(x, y):
    return Text((x, y), Fonts.LABEL_SMALL, Colors.TITLE, "lt")


def large(x, y, accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_LARGE, color, "rt")


def status(x, y, anchor="lm"):
    return Text((x, y), Fonts.STATUS, Colors.TITLE, anchor)


def destination(x, y):
    return Text((x, y), Fonts.STATUS, Colors.SECONDARY, "lt")


def departutes(x, y):
    return Text((x, y), Fonts.DEPARTURES, Colors.DEPARTURES, "rt")
