from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def clock(x, y):
    return Text((x, y), Fonts.CLOCK)


def temp_now(x, y):
    return Text((x, y), Fonts.WEATHER_TODAY)


def small(x, y, anchor="rt"):
    return Text((x, y), Fonts.LABEL_SMALL, Colors.SECONDARY, anchor)


def x_small(x, y, anchor="rt"):
    return Text((x, y), Fonts.LABEL_XSMALL, Colors.SECONDARY, anchor)


def title(x, y):
    return Text((x, y), Fonts.LABEL_SMALL, Colors.TITLE, "lt")


def large(x, y):
    return Text((x, y), Fonts.LABEL_LARGE, Colors.SECONDARY, "rt")


def status(x, y, anchor="lm"):
    return Text((x, y), Fonts.STATUS, Colors.TITLE, anchor)


def destination(x, y):
    return Text((x, y), Fonts.STATUS, Colors.SECONDARY, "lt")


def departutes(x, y):
    return Text((x, y), Fonts.DEPARTURES, Colors.DEPARTURES, "rt")
