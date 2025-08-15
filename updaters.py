from core.data_sources import Local, fetch_weather


# Run every 1 sec
def time_date() -> dict:
    return {
        "clock_image": f"./shared/images/clock/{Local.daytime()}.png",
        "time": Local.time(format="%H:%M"),
        "date_0": Local.time(format="%A"),
        "date_1": Local.time(format="%B %d")
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
    async def _day_or_night(j):
        now = Local.time()
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
        d = await _day_or_night(j)
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
        timestamps = []
        weather_items = []
        for entry in j["list"]:
            timestamps.append(Local.time(epoch=entry["dt"], format="%H:%M"))
            temp = round(entry["main"]["temp"])
            cond = entry["weather"][0]["main"]
            weather_items.append(
                f'{temp}°C, {cond}'
            )
        return ("\n".join(timestamps), "\n".join(weather_items))

    async def _mim_max(j):
        min = round(j["main"]["temp_min"])
        max = round(j["main"]["temp_max"])
        return f"↓ {min}°C   ↑ {max}°C"

    async def _wind(j):
        wind = j["wind"]["speed"]
        if wind > 0:
            return f"{wind} m/s"
        return ""

    data = await fetch_weather()
    hourly_data = await fetch_weather("hourly")
    hourly = await _hourly(hourly_data)

    return {
        "weather_image": await _weather_image(data),
        "hours": hourly[0],
        "values": hourly[1],
        "temp": await _temperature(data),
        "icon": await _current_icon(data),
        "feels_like": await _feels_like(data),
        "min_max": await _mim_max(data),
        "wind": await _wind(data)
    }


# Run every 1 min
async def trains() -> dict:
    return {}


async def buses() -> dict:
    return {}
