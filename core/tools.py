from time import time


def ticks(shift=0):
    return time() + shift


class IntervalLoop:
    def __init__(self, interval):
        self.interval = interval
        self.next_loop = ticks(interval)

    def done(self):
        if time() > self.next_loop:
            self.next_loop = ticks(self.interval)
            return True
        return False
