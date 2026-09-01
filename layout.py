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
            xy=(1208, 24), size=(688, 1112), fill=Colors.panel_bg, radius=32,
            content={
                "bg":      ImageView(),
                "temp":    Text(xy=(64, 34), **TextStyles.temperature),
                "icon":    ImageView(498, 90),
                "desc":    Text(xy=(64, 262), **TextStyles.weather_cond),
                "more":    Text(xy=(64, 318), **TextStyles.details),
                "icon_sr": Text(xy=(64, 362), **TextStyles.icon,
                                value="\uf051"),
                "sunrise": Text(xy=(128, 372), **TextStyles.details),
                "icon_ss": Text(xy=(286, 362), **TextStyles.icon,
                                value="\uf052"),
                "sunset":  Text(xy=(350, 372), **TextStyles.details),
                "hours":   Text(xy=(70, 504), **TextStyles.hours),
                "icons":   Text(xy=(196, 500), **TextStyles.weather_icons),
                "temps":   Text(xy=(280, 504), **TextStyles.temps),
                "station": Text(xy=(64, 850), **TextStyles.station)
            }
        ),
        "updater": updaters.weather,
        "int_s": 900
    },
    {
        "name": "Departures",
        "widget": Widget(
            xy=(24, 24), size=(1160, 1112), fill=Colors.panel_bg,
            radius=32,
            content={
                "time": Text(xy=(132, 24), **TextStyles.header_time),
                "date": Text(xy=(500, 66), **TextStyles.header_date),
                "city_title": Text(xy=(48, 158), **TextStyles.transport_title, value="TILL CITY"),
                "city_buses": Text(xy=(48, 202), **TextStyles.transport_rows),
                "city_divider": Rect((48, 390, 1200, 392), fill=Colors.tetriary, radius=1),
                "journey_title": Text(xy=(48, 422), **TextStyles.transport_title, value="TILL T-CENTRALEN"),
                "journeys": Text(xy=(48, 470), **TextStyles.journey_rows),
                "journey_divider": Rect((48, 800, 1200, 802), fill=Colors.tetriary, radius=1),
                "other_title": Text(xy=(48, 832), **TextStyles.transport_title, value="ÖVRIGA AVGÅNGAR"),
                "other_buses": Text(xy=(48, 878), **TextStyles.transport_rows),
            }
        ),
        "updater": updaters.departures,
        "int_s": 1
    }
]
