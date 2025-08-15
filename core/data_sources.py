import os
from datetime import datetime
from locale import setlocale, LC_ALL

import logging
import aiohttp
import async_timeout

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OWM_API_KEY = os.environ.get("OWM_API_KEY")
SL_API_KEY = os.environ.get("SL_API_KEY")

setlocale(LC_ALL, "sv_SE.UTF-8")

DEFAULT_TIMEOUT = 15  # seconds


async def fetch_json(url, params=None, headers=None, timeout=DEFAULT_TIMEOUT):
    try:
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(timeout):
                async with session.get(
                    url, params=params, headers=headers
                ) as resp:
                    resp.raise_for_status()
                    return await resp.json()
    except Exception as e:
        logging.warning(f"[aiorequests] Failed to fetch {url}: {e}")
        return None


class Local:
    from subprocess import check_output

    @staticmethod
    def time(format=None) -> str:
        if not format:
            return int(datetime.now().timestamp())
        return datetime.now().strftime(format)

    @staticmethod
    def hours() -> int:
        return datetime.now().hour

    @staticmethod
    def daytime() -> str:
        h = Local.hours()
        if h in range(5, 11):
            return "morning"
        elif h in range(11, 17):
            return "day"
        elif h in range(17, 22):
            return "evening"
        else:
            return "night"

    @staticmethod
    def day_or_night() -> str:
        if Local.hours() in range(6, 18):
            return "day"
        return "night"

    @staticmethod
    def hostname(flags="") -> str:
        if len(flags) > 0:
            flags = " " + flags
        return Local.check_output(
            f"hostname{flags}", shell=True, encoding="utf-8"
        ).split()[0]

    @staticmethod
    def ssid() -> str:
        return Local.check_output(
            "iwgetid -r", shell=True, encoding="utf-8"
        ).strip()

    @staticmethod
    def cpu() -> str:
        """Returns Temp, Load 1m, Load 5m, Load 15m"""
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            cpu_t = float(f.read())/1000
        with open("/proc/loadavg") as f:
            load1, load5, load15 = map(float, f.read().split()[:3])
        return cpu_t, load1, load5, load15

    @staticmethod
    def ram() -> str:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    ram = int(line.split()[1]) // 1024
                    break
                else:
                    pass
        return ram


class Commute:
    def get_trains():
        pass

# Weather data


async def fetch_weather(segment="current"):
    WEATHER_API = {
        "current": {
            "url": "https://api.openweathermap.org/data/2.5/weather",
            "params": {
                "units": "metric",
                "lat": 59.421491,
                "lon": 17.819238,
                "appid": OWM_API_KEY
            }
        },
        "hourly": {
            "url": "https://api.openweathermap.org/data/2.5/forecast",
            "params": {
                "cnt": 4,
                "units": "metric",
                "lat": 59.421491,
                "lon": 17.819238,
                "appid": OWM_API_KEY
            }
        }
    }
    API_REF = WEATHER_API[segment]
    data = await fetch_json(
        url=API_REF["url"],
        params=API_REF["params"]
    )
    return data
