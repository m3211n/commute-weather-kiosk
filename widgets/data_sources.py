from datetime import datetime
from locale import setlocale, LC_ALL

setlocale(LC_ALL, "sv_SE.UTF-8")


def get_time(format):
    """Simply returns current time us strftime(format)"""
    return datetime.now().strftime(format)


def get_system_info():
    import subprocess as s

    # IP address
    try:
        ip = s.check_output(
            "hostname -I", shell=True, encoding="utf-8"
        ).split()[0]
    except Exception:
        ip = "N/A"

    # Wi-Fi SSID
    try:
        ssid = s.check_output(
            "iwgetid -r", shell=True, encoding="utf-8"
        ).strip()
        if not ssid:
            ssid = "N/A"
    except Exception:
        ssid = "N/A"

    # CPU temperature
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            cpu_t = f"{float(f.read())/1000:.1f}°C"
    except Exception:
        cpu_t = "N/A"

    # RAM usage (free/total in MB)
    with open("/proc/meminfo") as f:
        ram = "N/A"
        for line in f:
            if line.startswith("MemAvailable:"):
                ram = int(line.split()[1]) // 1024
                break
            else:
                pass

    return f"SSID: {ssid} ({ip}) | CPU: {cpu_t} | Available RAM: {ram} MB"
