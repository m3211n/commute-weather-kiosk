from core.ui import Text
from shared.styles import Fonts, Colors
# import logging


def clock(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.CLOCK,
        color=Colors.DEFAULT,
        anchor=anchor)


def temp_now(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.WEATHER_TODAY,
        color=Colors.DEFAULT,
        anchor=anchor)


def small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_SMALL,
        color=color,
        anchor=anchor)


def small_block(x, y, accent=False, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_SMALL,
        color=color,
        **kwargs)


def x_small(x, y, anchor="rt", accent=False):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_XSMALL,
        color=color,
        anchor=anchor)


def title(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_SMALL,
        color=Colors.TITLE,
        anchor=anchor)


def large(x, y, accent=False, anchor="lt"):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=Fonts.LABEL_LARGE,
        color=color,
        anchor=anchor)


def status(x, y, anchor="lm"):
    return Text(
        xy=(x, y),
        font=Fonts.STATUS,
        color=Colors.TITLE,
        anchor=anchor)


def destination(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.STATUS,
        color=Colors.SECONDARY,
        anchor=anchor)


def departutes(x, y, anchor="lt"):
    return Text(
        xy=(x, y),
        font=Fonts.DEPARTURES,
        color=Colors.DEPARTURES,
        anchor=anchor)
