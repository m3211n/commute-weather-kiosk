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
        "name": "Weather",
        "widget": Widget(
            xy=(1296, 24), size=(600, 1088), fill=Colors.panel_bg, radius=32,
            content={
                "bg":      ImageView(),
                "temp":    Text(xy=(48, 24), **TextStyles.temperature),
                "icon":    ImageView(398, 62),
                "desc":    Text(xy=(48, 224), **TextStyles.weather_cond),
                "more":    Text(xy=(48, 274), **TextStyles.details),
                "icon_sr": Text(xy=(48, 318), **TextStyles.icon,
                                value="\uf051"),
                "sunrise": Text(xy=(112, 328), **TextStyles.details),
                "icon_ss": Text(xy=(284, 318), **TextStyles.icon,
                                value="\uf052"),
                "sunset":  Text(xy=(348, 328), **TextStyles.details),
                "hours":   Text(xy=(40, 420), **TextStyles.hours_compact),
                "icons":   Text(xy=(150, 416), **TextStyles.weather_icons_compact),
                "temps":   Text(xy=(226, 420), **TextStyles.temps_compact),
                "station": Text(xy=(48, 852), **TextStyles.station)
            }
        ),
        "updater": updaters.weather,
        "int_s": 900
    },
    {
        "name": "Departures",
        "widget": Widget(
            xy=(24, 24), size=(1248, 1088), fill=Colors.panel_bg,
            radius=32,
            content={
                "time": Text(xy=(132, 24), **TextStyles.header_time),
                "date": Text(xy=(500, 66), **TextStyles.header_date),
                "city_title": Text(xy=(48, 158), **TextStyles.transport_title, value="TILL CITY"),
                "city_buses": Text(xy=(48, 202), **TextStyles.transport_rows),
                "city_divider": Rect((48, 340, 1200, 342), fill=Colors.tetriary, radius=1),
                "journey_title": Text(xy=(48, 370), **TextStyles.transport_title, value="TILL T-CENTRALEN"),
                "journeys": Text(xy=(48, 418), **TextStyles.journey_rows),
                "journey_divider": Rect((48, 748, 1200, 750), fill=Colors.tetriary, radius=1),
                "other_title": Text(xy=(48, 780), **TextStyles.transport_title, value="ÖVRIGA AVGÅNGAR"),
                "other_buses": Text(xy=(48, 826), **TextStyles.transport_rows),
            }
        ),
        "updater": updaters.departures,
        "int_s": 1
    }
]
