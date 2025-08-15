from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def clock(x, y, anchor="lt"):
    return Text((x, y), Fonts.CLOCK, Colors.DEFAULT, anchor)


def temp_now(x, y, anchor="lt"):
    return Text((x, y), Fonts.WEATHER_TODAY, Colors.DEFAULT, anchor)


def small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_SMALL, color, anchor)


def small_block(x, y, accent=False, anchor="lt"):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_SMALL, color)


def x_small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_XSMALL, color, anchor)


def title(x, y, anchor="lt"):
    return Text((x, y), Fonts.LABEL_SMALL, Colors.TITLE, anchor)


def large(x, y, accent=False, anchor="lt"):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text((x, y), Fonts.LABEL_LARGE, color, anchor)


def status(x, y, anchor="lm"):
    return Text((x, y), Fonts.STATUS, Colors.TITLE, anchor)


def destination(x, y, anchor="lt"):
    return Text((x, y), Fonts.STATUS, Colors.SECONDARY, anchor)


def departutes(x, y, anchor="lt"):
    return Text((x, y), Fonts.DEPARTURES, Colors.DEPARTURES, anchor)
