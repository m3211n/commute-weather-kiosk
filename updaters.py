from core.data_sources import Local, fetch_weather, fetch_departures

TIME_F_STR = "%H:%M"
DATE_F_STR = "%A, %B %d"


# Run every 1 sec
def time_date() -> dict:
    return {
        "clock_image": f"./shared/images/clock/{Local.daytime()}.png",
        "time": Local.f_time(format=TIME_F_STR),
        "date": Local.f_time(format=DATE_F_STR).title()
    }


# Run every 1 sec
def sys_info() -> dict:
    host_values = [
        f"WI-FI SSID: {Local.ssid()}",
        f"IPv4: {Local.hostname('-I')}",
        Local.hostname()
    ]
    sys_values = [
        f"Available RAM: {Local.ram()} MB",
        f"CPU Temp: {Local.cpu()[0]:.1f}°C",
        f"CPU Load: {round(Local.cpu()[1] * 100, 1)}%"
    ]
    return {
        "host_info": " | ".join(host_values),
        "sys_info": " | ".join(sys_values)
    }


# Run every 15 min
async def weather() -> dict:

    def _weather_image(j) -> str:

        clouds = j["clouds"]["all"]
        if clouds in range(0, 33):
            c = "clear"
        elif clouds in range(33, 66):
            c = "cloudy"
        else:
            c = "rainy"

        if Local.epoch() in range(j["sys"]["sunrise"], j["sys"]["sunset"]):
            d = "day"
        else:
            d = "night"
        return f"./shared/images/weather/{c}-{d}.png"

    def _temperature(j) -> str:
        temp = round(j["main"]["temp"])
        return f"{temp}°"

    def _current_icon(j) -> str:
        icon = j["weather"][0]["icon"]
        return f"./shared/icons/weather/{icon}.png"

    def _desc(j) -> str:
        desc: str = j["weather"][0]["description"]
        return desc.capitalize()

    def _sun(j) -> str:
        sunrise = j["sys"]["sunrise"]
        sunset = j["sys"]["sunset"]
        return (
            Local.f_time(sunrise, TIME_F_STR),
            Local.f_time(sunset, TIME_F_STR)
        )

    def _hourly(j):
        timestamps = []
        temps = []
        icons = []

        for entry in j["list"]:
            timestamps.append(Local.f_time(entry["dt"], TIME_F_STR))
            temp = round(entry["main"]["temp"])
            wind = round(entry["wind"]["speed"], 1)
            icon = entry["weather"][0]["icon"]
            temps.append(
                f'{temp}°C   {wind} m/s'
            )
            icons.append(
                f"{_weather_icon_font(icon)}"
            )
        return ("\n".join(timestamps), "\n".join(temps), "\n".join(icons))

    def _more(j) -> str:
        min = round(j["main"]["temp_min"])
        max = round(j["main"]["temp_max"])
        temp = round(j["main"]["feels_like"])
        wind = round(j["wind"]["speed"], 1)
        return f"Känns som {temp}° (H:{max}° L:{min}°) {wind} m/s"

    def _weather_icon_font(icon):
        icon_font = {
            "01d": "\uf00d",
            "01n": "\uf02e",
            "02d": "\uf002",
            "02n": "\uf086",
            "03d": "\uf041",
            "03n": "\uf041",
            "04d": "\uf013",
            "04n": "\uf013",
            "09d": "\uf01a",
            "09n": "\uf01a",
            "10d": "\uf019",
            "10n": "\uf019",
            "11d": "\uf01d",
            "11n": "\uf01d",
            "13d": "\uf01b",
            "13n": "\uf01b",
            "50d": "\uf014",
            "50n": "\uf014"
        }
        return icon_font[icon]

    data = await fetch_weather()
    hourly_data = await fetch_weather("hourly")
    hourly = _hourly(hourly_data)
    sun = _sun(data)

    return {
        "weather_image": _weather_image(data),
        "temp": _temperature(data),
        "icon": _current_icon(data),
        "desc": _desc(data),
        "more": _more(data),
        "sunrise": sun[0],
        "sunset": sun[1],
        "hours": hourly[0],
        "temps": hourly[1],
        "icons": hourly[2],
    }


# Run every 1 min
async def departures() -> dict:
    # import json

    BUS_STOP_POINT = 51583

    data_trains = await fetch_departures()
    data_buses = [
        d for d in await fetch_departures("bus")
        if d.get("stop_point", {}).get("id") == BUS_STOP_POINT
    ]

    # print(json.dumps(data_buses, indent=2, ensure_ascii=False))

    def _extract_lists(data):
        display = []
        line = []
        dest = []
        count = 0
        for departure in data:
            if departure["state"] != "EXPECTED":
                continue
            display.append(departure["display"])
            line.append(departure["line"]["designation"])
            dest.append(departure["destination"])
            count = count + 1
            if count == 3:
                break
        return {
            "display": "\n".join(display),
            "line": "\n".join(line),
            "dest": "\n".join(dest)
        }

    train_info = _extract_lists(data_trains)
    bus_info = _extract_lists(data_buses)

    return {
        "train_display": train_info["display"],
        "train_line": train_info["line"],
        "train_dest": train_info["dest"],
        "bus_display": bus_info["display"],
        "bus_line": bus_info["line"],
        "bus_dest": bus_info["dest"],
    }
