from datetime import datetime
from locale import setlocale, LC_ALL

setlocale(LC_ALL, "sv_SE.UTF-8")


def get_time(format):
    """Simply returns current time us strftime(format)"""
    return datetime.now().strftime(format)
