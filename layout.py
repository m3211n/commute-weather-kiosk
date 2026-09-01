import updaters
from core.ui import (
    Widget, ImageView, Rect, Text,
)
from core.styles import Colors, TextStyles

WIDGETS = [
    {
        "name": "Info",
        "widget": Widget(
            xy=(0, 1136), size=(1920, 64), fill=(0, 0, 0, 255),
            content={
                "host_info": Text(xy=(16, 18), **TextStyles.status_small),
                "sys_info":  Text(xy=(16, 46), **TextStyles.status_small),
                "freshness": Text(xy=(1888, 32), **TextStyles.status_rt)
            }
        ),
        "updater": updaters.sys_info,
        "int_s": 5
    },
    {
        "name": "Clock",
        "widget": Widget(
            xy=(24, 24), size=(1872, 112), fill=Colors.panel_bg, radius=32,
            content={
                "time": Text(xy=(185, 18), **TextStyles.header_time),
                "date": Text(xy=(450, 56), **TextStyles.header_date)
            }
        ),
        "updater": updaters.time_date,
        "int_s": 1
    },
    {
        "name": "Weather",
        "widget": Widget(
            xy=(1208, 160), size=(688, 952), fill=Colors.panel_bg, radius=32,
            content={
                "bg":      ImageView(),
                "temp":    Text(xy=(48, 24), **TextStyles.temperature),
                "icon":    ImageView(470, 62),
                "desc":    Text(xy=(48, 224), **TextStyles.weather_cond),
                "more":    Text(xy=(48, 274), **TextStyles.details),
                "icon_sr": Text(xy=(48, 318), **TextStyles.icon,
                                value="\uf051"),
                "sunrise": Text(xy=(112, 328), **TextStyles.details),
                "icon_ss": Text(xy=(284, 318), **TextStyles.icon,
                                value="\uf052"),
                "sunset":  Text(xy=(348, 328), **TextStyles.details),
                "hours":   Text(xy=(48, 420), **TextStyles.hours_compact),
                "icons":   Text(xy=(172, 416), **TextStyles.weather_icons_compact),
                "temps":   Text(xy=(250, 420), **TextStyles.temps_compact),
                "station": Text(xy=(48, 852), **TextStyles.station)
            }
        ),
        "updater": updaters.weather,
        "int_s": 900
    },
    {
        "name": "Departures",
        "widget": Widget(
            xy=(24, 160), size=(1160, 952), fill=Colors.panel_bg,
            radius=32,
            content={
                "city_title": Text(xy=(48, 42), **TextStyles.transport_title, value="TILL CITY"),
                "city_buses": Text(xy=(48, 86), **TextStyles.transport_rows),
                "city_divider": Rect((48, 224, 1112, 226), fill=Colors.tetriary, radius=1),
                "journey_title": Text(xy=(48, 254), **TextStyles.transport_title, value="TILL T-CENTRALEN"),
                "journeys": Text(xy=(48, 302), **TextStyles.journey_rows),
                "journey_divider": Rect((48, 600, 1112, 602), fill=Colors.tetriary, radius=1),
                "other_title": Text(xy=(48, 632), **TextStyles.transport_title, value="ÖVRIGA AVGÅNGAR"),
                "other_buses": Text(xy=(48, 678), **TextStyles.transport_rows),
            }
        ),
        "updater": updaters.departures,
        "int_s": 60
    }
]
