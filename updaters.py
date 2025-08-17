from core.data_sources import Local, fetch_weather


# Run every 1 sec
def time_date() -> dict:
    return {
        "clock_image": f"./shared/images/clock/{Local.daytime()}.png",
        "time": Local.f_time(format="%H:%M"),
        "date": Local.f_time(format="%A, %B %d").title()
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
    def _day_or_night(j):
        now = Local.epoch()
        if now in range(j["sys"]["sunrise"], j["sys"]["sunset"]):
            return "day"
        return "night"

    async def _weather_image(j):
        clouds = j["clouds"]["all"]
        if clouds in range(0, 33):
            c = "clear"
        elif clouds in range(33, 66):
            c = "cloudy"
        else:
            c = "rainy"
        d = _day_or_night(j)
        # icon = weather["icon"]
        return f"./shared/images/weather/{c}-{d}.png"

    async def _temperature(j):
        temp = round(j["main"]["temp"])
        return f"{temp}°"

    async def _current_icon(j):
        icon = j["weather"][0]["icon"]
        return f"./shared/icons/weather/{icon}.png"

    async def _feels_like(j):
        temp = round(j["main"]["feels_like"])
        return f"Känns som {temp}°C"

    async def _hourly(j):

        f_str = "%H:%M"
        sunrise = j["city"]["sunrise"]
        sunset = j["city"]["sunset"]
        sunrise_added = False
        sunset_added = False
        prev_ts = Local.epoch()

        timestamps = []
        temps = []
        icons = []

        for entry in j["list"]:
            if entry["dt"] > sunrise > prev_ts and not sunrise_added:
                timestamps.append(Local.f_epoch(sunrise, f_str))
                temps.append("Soluppgång")
                icons.append("\uf051")
                sunrise_added = True
            if entry["dt"] > sunset > prev_ts and not sunset_added:
                timestamps.append(Local.f_epoch(sunset, f_str))
                temps.append("Solnedgång")
                icons.append("\uf052")
                sunset_added = True
            prev_ts = entry["dt"]
            timestamps.append(Local.f_epoch(entry["dt"], f_str))
            temp = round(entry["main"]["temp"])
            icon = entry["weather"][0]["icon"]
            temps.append(
                f'{temp}°C'
            )
            icons.append(
                f"{_weather_icon_font(icon)}"
            )
        return ("\n".join(timestamps), "\n".join(temps), "\n".join(icons))

    async def _mim_max_wind(j):
        min = round(j["main"]["temp_min"])
        max = round(j["main"]["temp_max"])
        wind = j["wind"]["speed"]
        return f"H:{max}° L:{min}° {wind} m/s"

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

    hourly = await _hourly(hourly_data)

    return {
        "weather_image": await _weather_image(data),
        "hours": hourly[0],
        "temps": hourly[1],
        "icons": hourly[2],
        "temp": await _temperature(data),
        "icon": await _current_icon(data),
        "feels_like": await _feels_like(data),
        "min_max_wind": await _mim_max_wind(data)
    }


# Run every 1 min
async def trains() -> dict:
    return {}


async def buses() -> dict:
    return {}
