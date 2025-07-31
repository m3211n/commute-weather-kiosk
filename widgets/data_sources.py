from datetime import datetime
from time import time
from locale import setlocale, LC_ALL
import subprocess as s


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
