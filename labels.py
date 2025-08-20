from core.ui import Text
from shared.styles import font, Colors
# import logging


def time(x, y):
    return Text(
        xy=(x, y),
        font=font("bold", 216),
        fill=Colors.DEFAULT,
        anchor="mt")


def date(x, y):
    return Text(
        xy=(x, y),
        font=font("bold", 40),
        fill=Colors.DEFAULT,
        anchor="mt")


def temp_now(x, y):
    return Text(
        xy=(x, y),
        font=font("light", 200),
        anchor="lt",
        fill=Colors.DEFAULT)


def status(x, y, **kwargs):
    return Text(
        xy=(x, y),
        font=font("mono", 22),
        fill=Colors.TETRIARY,
        **kwargs)


def departures(x, y):
    return Text(
        xy=(x, y),
        font=font("bold", 48),
        fill=Colors.DEPARTURES,
        spacing=16,
        features=["tnum"]
    )


def lines(x, y):
    return regular(x=x, y=y, size=48, spacing=16)


def destinations(x, y):
    return regular(x=x, y=y, size=48, accent=False, spacing=16)


def regular(x, y, size: int, accent=True, **kwargs):
    color = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=font("regular", size),
        fill=color,
        features=["tnum"],
        **kwargs)


def icon(x, y, accent=True, **kwargs):
    fill = Colors.DEFAULT if accent else Colors.SECONDARY
    return Text(
        xy=(x, y),
        font=font("icon", 36),
        fill=fill,
        **kwargs)
