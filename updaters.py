from datetime import datetime

from core.data_sources import Local
from core.mqtt_data import data as mqtt_data

DATE_F_STR = "%A, %B %-d"


# Run every 1 sec
def time_date() -> dict:
    return {
        # "bg": f"./assets/images/clock/{Local.daytime()}.png",
        "time": Local.f_time(),
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
    weather_updated = mqtt_data.updated_at("weather/current")
    transit_updated = mqtt_data.updated_at("transit/city-buses")

    def freshness(name, timestamp):
        return f"{name}: {timestamp[11:16]}" if timestamp else f"{name}: waiting"

    return {
        "host_info": " | ".join(host_values),
        "sys_info": " | ".join(sys_values),
        "freshness": "  ".join((
            freshness("Weather", weather_updated),
            freshness("Transit", transit_updated),
        )),
    }


# Run every 15 min
def weather() -> dict:
    data = mqtt_data.snapshot("weather/current", {})
    hourly_data = mqtt_data.snapshot("weather/forecast", [])
    sun_data = mqtt_data.snapshot("weather/solar", {})
    if not data:
        return {
            "bg": "./assets/images/weather/cloudy-day.png", "temp": "--°",
            "icon": "./assets/icons/weather/03d.png", "desc": "Väntar på MQTT",
            "more": "", "sunrise": "--:--", "sunset": "--:--",
            "hours": "", "temps": "", "icons": "", "station": "",
        }
    icon_font = {
        "01d": "\uf00d", "01n": "\uf02e", "02d": "\uf002", "02n": "\uf086",
        "03d": "\uf041", "03n": "\uf041", "04d": "\uf013", "04n": "\uf013",
        "09d": "\uf01a", "09n": "\uf01a", "10d": "\uf019", "10n": "\uf019",
        "11d": "\uf01d", "11n": "\uf01d", "13d": "\uf01b", "13n": "\uf01b",
        "50d": "\uf014", "50n": "\uf014",
    }
    hourly = (
        "\n".join(Local.f_time(entry["time"]) for entry in hourly_data),
        "\n".join(f"{entry['temperature_c']}°C  {entry['wind_mps']} m/s" for entry in hourly_data),
        "\n".join(icon_font.get(entry["icon"], "\uf041") for entry in hourly_data),
    )
    sun = (
        Local.f_time(datetime.fromisoformat(sun_data["sunrise"]).timestamp())
        if sun_data.get("sunrise") else "--:--",
        Local.f_time(datetime.fromisoformat(sun_data["sunset"]).timestamp())
        if sun_data.get("sunset") else "--:--",
    )
    station = "Weather station: {} C  {}%  {} hPa".format(
        mqtt_data.get("weather/outdoor/temperature", "--"),
        mqtt_data.get("weather/outdoor/humidity", "--"),
        mqtt_data.get("weather/outdoor/pressure", "--"),
    )

    return {
        "bg": f"./assets/images/weather/cloudy-{Local.daytime() if Local.daytime() in ('day', 'night') else 'day'}.png",
        "temp": f"{data['temperature_c']}°",
        "icon": f"./assets/icons/weather/{data['icon']}.png",
        "desc": data["location"],
        "more": "Känns som {feels_like_c}° (H:{maximum_c}° L:{minimum_c}°) {wind_mps} m/s".format(**data),
        "sunrise": sun[0],
        "sunset": sun[1],
        "hours": hourly[0],
        "temps": hourly[1],
        "icons": hourly[2],
        "station": station,
    }


def departures() -> dict:
    def short(value, length=32):
        return value if len(value) <= length else f"{value[:length - 1]}…"

    def render_buses(items):
        return "\n".join(
            f"{item['line']:>4}  {item['destination']:<24} {item['departure']:>8}"
            for item in items
        ) or "Väntar på MQTT"

    def render_journeys(items):
        rows = []
        for item in items:
            rows.append(
                "{bus_departure_time}  {bus_line_number}  {bus_line_destination}"
                "\n      transfer {transfer_minutes} min"
                "\n{train_departure_time}  {train_line_number}  {train_destination}".format(
                    bus_departure_time=item.get("bus_departure_time", "--:--"),
                    bus_line_number=item.get("bus_line_number", "?"),
                    bus_line_destination=short(item.get("bus_line_destination", "")),
                    transfer_minutes=item.get("transfer_minutes") or "?",
                    train_departure_time=item.get("train_departure_time", "--:--"),
                    train_line_number=item.get("train_line_number", "?"),
                    train_destination=short(item.get("train_destination", "")),
                )
            )
        return "\n\n".join(rows) or "Väntar på MQTT"

    return {
        "city_buses": render_buses(mqtt_data.snapshot("transit/city-buses", [])),
        "journeys": render_journeys(mqtt_data.snapshot("transit/journeys", [])),
        "other_buses": render_buses(mqtt_data.snapshot("transit/other-buses", [])),
    }
