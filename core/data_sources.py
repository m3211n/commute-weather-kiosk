from datetime import datetime
from time import time
from locale import setlocale, LC_ALL
import subprocess as s

from core.links import SL_TRAINS, WEATHER_HOURLY

setlocale(LC_ALL, "sv_SE.UTF-8")


class Tools:
    @staticmethod
    def time():
        return time()


class Local:

    @staticmethod
    def time(format) -> str:
        return datetime.now().strftime(format)

    @staticmethod
    def hours() -> int:
        return datetime.now().hour

    @staticmethod
    def daytime() -> str:
        h = datetime.now().hour
        if 6 <= h < 11:
            daytime_str = "morning"
        elif 11 <= h < 15:
            daytime_str = "day"
        elif 15 <= h < 20:
            daytime_str = "evening"
        else:
            daytime_str = "night"
        return daytime_str

    @staticmethod
    def day_night() -> str:
        h = datetime.now().hour
        if 6 <= h < 18:
            daytime_str = "day"
        else:
            daytime_str = "night"
        return daytime_str

    @staticmethod
    def hostname(flags="") -> str:
        if len(flags) > 0:
            flags = " " + flags
        return s.check_output(
            f"hostname{flags}", shell=True, encoding="utf-8"
        ).split()[0]

    @staticmethod
    def ssid() -> str:
        return s.check_output(
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
        return f"{ram} MB"


class Commute:
    def get_trains(self, url=SL_TRAINS):
        pass


class WeatherData:
    @staticmethod
    def get_current(url=WEATHER_HOURLY):
        return "24", "Clear"
