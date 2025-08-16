from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def clock(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.CLOCK,
        fill=Colors.DEFAULT,
        anchor=anchor)


def temp_now(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.WEATHER_TODAY,
        fill=Colors.DEFAULT,
        anchor=anchor)


def small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_SMALL,
        fill=color,
        anchor=anchor)


def small_b(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_BOLD,
        fill=color,
        anchor=anchor)


def x_small_block(x, y, accent=False, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_XSMALL,
        fill=color,
        features=["tnum"],
        **kwargs)


def x_small_block_icons(x, y, accent=False, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.ICON_XSMALL,
        fill=color,
        features=["tnum"],
        **kwargs)


def x_small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_XSMALL,
        fill=color,
        features=["tnum"],
        anchor=anchor)


def title(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_SMALL,
        fill=Colors.TITLE,
        anchor=anchor)


def large(x, y, accent=False, anchor="lt"):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_LARGE,
        fill=color,
        anchor=anchor)


def status(x, y, anchor="lm"):
    return Text(
        xy=(x, y),
        font=Fonts.STATUS,
        fill=Colors.TITLE,
        anchor=anchor)


def destination(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.STATUS,
        fill=Colors.SECONDARY,
        anchor=anchor)


def departutes(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.DEPARTURES,
        fill=Colors.DEPARTURES,
        anchor=anchor)
